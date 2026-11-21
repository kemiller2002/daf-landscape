/// Partner-federated identity, MFA assurance and access decisions (DD-021).
/// Pure policy: the same request, session and configuration always give the same decision.
/// Assurance levels follow NIST SP 800-63B (AAL1/2/3); "phishing-resistant" is tracked separately
/// because a TOTP code is AAL2 but not phishing-resistant, while a passkey/WebAuthn is.
module Daf.Enterprise.Identity

open System

type OrgId = OrgId of string
type UserId = UserId of string
type ClientId = ClientId of string

/// How a partner organization (which owns the client relationship and the accounts in its program)
/// federates with the platform.
type PartnerTrust =
    { Org: OrgId
      Protocol: string                 // "OIDC" | "SAML"
      MfaAttestedByContract: bool      // the partner contractually attests its MFA policy and passes amr/acr
      AcceptedAmr: Set<string>         // e.g. "hwk", "phr", "mfa", "otp" (RFC 8176 values)
      ScimProvisioning: bool }         // joiners/leavers pushed by the partner

type Method =
    | LocalPasskey                     // WebAuthn/FIDO2 at the platform
    | LocalTotp
    | LocalPasswordOnly
    | PartnerFederated of OrgId * amr: Set<string>

type Assurance = { Aal: int; PhishingResistant: bool }

type Session =
    { User: UserId
      Org: OrgId option                // partner organization membership, if any
      Method: Method
      AuthenticatedAt: DateTime
      Active: bool }                   // false once SCIM (or the platform) deprovisions the user

type Role =
    | Donor
    | Advisor
    | PartnerAdmin
    | SponsorStaff of privileged: bool

type Principal = { Session: Session; Role: Role }

/// A machine client of a partner (system-to-system API access).
type MachineClient =
    { Client: ClientId
      Org: OrgId
      MtlsBound: bool                  // certificate-bound access token (RFC 8705) or DPoP (RFC 9449)
      Scopes: Set<string> }

type Account = { Id: string; OwnerOrg: OrgId; Donor: UserId; Advisors: Set<UserId> }

type Action =
    | ViewAccount
    | RecommendGrant of amount: decimal
    | ChangeDelegation                 // add/remove an advisor or a donor-side agent
    | ManagePartnerUsers               // partner admin user management
    | ChangeRecoveryFactors            // account recovery: the classic MFA bypass
    | StaffPrivilegedOperation

type Requirement = { MinAal: int; PhishingResistant: bool; MaxAuthAge: TimeSpan option }

type Decision =
    | Allow
    | StepUp of Requirement            // RFC 9470: insufficient_user_authentication with acr_values / max_age
    | Deny of string

type Policy =
    { HighValueGrant: decimal          // above this a fresh phishing-resistant authentication is required [A]
      SensitiveMaxAge: TimeSpan }      // freshness for sensitive actions [A]

let defaultPolicy = { HighValueGrant = 25000m; SensitiveMaxAge = TimeSpan.FromMinutes 15.0 }

/// Assurance actually established by a session, given the platform's trust in partners.
/// A partner's MFA claim counts only if the partner is trusted for MFA AND the asserted amr values
/// are ones the platform accepts; otherwise the federated login is treated as single-factor.
let assurance (trusts: Map<OrgId, PartnerTrust>) (s: Session) : Assurance =
    match s.Method with
    | LocalPasskey -> { Aal = 2; PhishingResistant = true }
    | LocalTotp -> { Aal = 2; PhishingResistant = false }
    | LocalPasswordOnly -> { Aal = 1; PhishingResistant = false }
    | PartnerFederated(org, amr) ->
        match trusts.TryFind org with
        | Some t when t.MfaAttestedByContract ->
            let accepted = Set.intersect amr t.AcceptedAmr
            if accepted.Contains "hwk" || accepted.Contains "phr" then { Aal = 2; PhishingResistant = true }
            elif accepted.Contains "mfa" || accepted.Contains "otp" then { Aal = 2; PhishingResistant = false }
            else { Aal = 1; PhishingResistant = false }
        | _ -> { Aal = 1; PhishingResistant = false }

let requirement (p: Policy) (a: Action) : Requirement =
    match a with
    | ViewAccount -> { MinAal = 2; PhishingResistant = false; MaxAuthAge = None }
    | RecommendGrant amt when amt > p.HighValueGrant -> { MinAal = 2; PhishingResistant = true; MaxAuthAge = Some p.SensitiveMaxAge }
    | RecommendGrant _ -> { MinAal = 2; PhishingResistant = false; MaxAuthAge = None }
    | ChangeDelegation
    | ChangeRecoveryFactors
    | ManagePartnerUsers -> { MinAal = 2; PhishingResistant = true; MaxAuthAge = Some p.SensitiveMaxAge }
    | StaffPrivilegedOperation -> { MinAal = 2; PhishingResistant = true; MaxAuthAge = Some p.SensitiveMaxAge }

let private meets (now: DateTime) (s: Session) (have: Assurance) (r: Requirement) =
    have.Aal >= r.MinAal
    && (not r.PhishingResistant || have.PhishingResistant)
    && (match r.MaxAuthAge with Some age -> now - s.AuthenticatedAt <= age | None -> true)

/// Relationship authorization: who may act on which account, independent of assurance.
let private authorized (pr: Principal) (acct: Account option) (a: Action) =
    let sameOrg = match pr.Session.Org, acct with Some o, Some ac -> o = ac.OwnerOrg | _ -> false
    match pr.Role, a, acct with
    | SponsorStaff true, StaffPrivilegedOperation, _ -> Ok()
    | SponsorStaff _, StaffPrivilegedOperation, _ -> Error "staff member lacks just-in-time privileged access"
    | _, StaffPrivilegedOperation, _ -> Error "only sponsor staff may perform privileged operations"
    | PartnerAdmin, ManagePartnerUsers, _ -> (match pr.Session.Org with Some _ -> Ok() | None -> Error "partner admin without organization")
    | _, ManagePartnerUsers, _ -> Error "only partner administrators manage partner users"
    | Donor, _, Some ac when ac.Donor = pr.Session.User -> Ok()
    | Donor, _, _ -> Error "donor may act only on own account"
    | Advisor, (ViewAccount | RecommendGrant _), Some ac when sameOrg && ac.Advisors.Contains pr.Session.User -> Ok()
    | Advisor, (ViewAccount | RecommendGrant _), Some _ when not sameOrg -> Error "account belongs to another partner organization"
    | Advisor, (ViewAccount | RecommendGrant _), _ -> Error "advisor holds no donor-consented privilege on this account"
    | Advisor, _, _ -> Error "advisors cannot change delegation or recovery; the donor must"
    | PartnerAdmin, _, _ -> Error "partner administrators manage users, not donor accounts"
    | SponsorStaff _, _, _ -> Error "staff act on accounts only through governed workflows"

/// Full decision: deprovisioning first, then relationship authorization, then assurance (step-up).
let decide (p: Policy) (trusts: Map<OrgId, PartnerTrust>) (now: DateTime) (pr: Principal) (acct: Account option) (a: Action) : Decision =
    if not pr.Session.Active then Deny "user deprovisioned"
    else
        match authorized pr acct a with
        | Error reason -> Deny reason
        | Ok() ->
            let req = requirement p a
            if meets now pr.Session (assurance trusts pr.Session) req then Allow else StepUp req

/// Machine-to-machine: partner systems may call partner-scope APIs only with sender-constrained tokens,
/// only for accounts their organization owns, and only within granted scopes.
let decideMachine (c: MachineClient) (acct: Account) (scope: string) : Decision =
    if not c.MtlsBound then Deny "token not sender-constrained (mTLS or DPoP required)"
    elif c.Org <> acct.OwnerOrg then Deny "account belongs to another partner organization"
    elif not (c.Scopes.Contains scope) then Deny $"scope {scope} not granted"
    else Allow
