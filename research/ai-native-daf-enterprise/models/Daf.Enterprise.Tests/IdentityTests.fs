module Daf.Enterprise.Tests.IdentityTests

open System
open Xunit
open Daf.Enterprise.Identity

let now = DateTime(2026, 11, 21, 12, 0, 0, DateTimeKind.Utc)
let wealthCo = OrgId "partner-wealthco"
let otherCo = OrgId "partner-otherco"

let trusts =
    Map.ofList
        [ wealthCo, { Org = wealthCo; Protocol = "OIDC"; MfaAttestedByContract = true; AcceptedAmr = set [ "hwk"; "phr"; "mfa"; "otp" ]; ScimProvisioning = true }
          otherCo, { Org = otherCo; Protocol = "SAML"; MfaAttestedByContract = false; AcceptedAmr = Set.empty; ScimProvisioning = false } ]

let acct = { Id = "A-1"; OwnerOrg = wealthCo; Donor = UserId "donor-1"; Advisors = set [ UserId "adv-1" ] }

let session user org meth ageMinutes =
    { User = UserId user; Org = org; Method = meth; AuthenticatedAt = now.AddMinutes(-ageMinutes); Active = true }

let advisor meth age = { Session = session "adv-1" (Some wealthCo) meth age; Role = Advisor }
let decide' pr a = decide defaultPolicy trusts now pr (Some acct) a

[<Fact>]
let ``partner-asserted phishing-resistant MFA is honoured when the partner is trusted`` () =
    Assert.Equal(Allow, decide' (advisor (PartnerFederated(wealthCo, set [ "pwd"; "hwk" ])) 5.0) (RecommendGrant 100000m))

[<Fact>]
let ``partner-asserted OTP satisfies AAL2 but not phishing-resistant high-value actions`` () =
    let pr = advisor (PartnerFederated(wealthCo, set [ "pwd"; "otp" ])) 5.0
    Assert.Equal(Allow, decide' pr (RecommendGrant 1000m))
    Assert.True(match decide' pr (RecommendGrant 100000m) with StepUp r -> r.PhishingResistant | _ -> false)

[<Fact>]
let ``an untrusted partner's MFA claim is ignored and the user must step up locally`` () =
    let pr = { Session = session "adv-9" (Some otherCo) (PartnerFederated(otherCo, set [ "mfa"; "hwk" ])) 1.0; Role = Advisor }
    let acctOther = { acct with Id = "A-9"; OwnerOrg = otherCo; Advisors = set [ UserId "adv-9" ] }
    Assert.True(match decide defaultPolicy trusts now pr (Some acctOther) ViewAccount with StepUp r -> r.MinAal = 2 | _ -> false)

[<Fact>]
let ``password-only login never reaches account data`` () =
    let donor = { Session = session "donor-1" None LocalPasswordOnly 1.0; Role = Donor }
    Assert.True(match decide' donor ViewAccount with StepUp _ -> true | _ -> false)

[<Fact>]
let ``stale authentication forces step-up for sensitive actions even with a passkey`` () =
    let donor = { Session = session "donor-1" None LocalPasskey 120.0; Role = Donor }
    Assert.Equal(Allow, decide' donor ViewAccount)
    Assert.True(match decide' donor ChangeDelegation with StepUp r -> r.MaxAuthAge.IsSome | _ -> false)
    let fresh = { Session = session "donor-1" None LocalPasskey 2.0; Role = Donor }
    Assert.Equal(Allow, decide' fresh ChangeDelegation)

[<Fact>]
let ``TOTP cannot change recovery factors (the MFA-bypass path needs phishing resistance)`` () =
    let donor = { Session = session "donor-1" None LocalTotp 1.0; Role = Donor }
    Assert.True(match decide' donor ChangeRecoveryFactors with StepUp r -> r.PhishingResistant | _ -> false)

[<Fact>]
let ``an advisor from another partner organization is denied regardless of assurance`` () =
    let pr = { Session = session "adv-1" (Some otherCo) LocalPasskey 1.0; Role = Advisor }
    Assert.True(match decide' pr ViewAccount with Deny r -> r.Contains "another partner" | _ -> false)

[<Fact>]
let ``an advisor without a donor-consented privilege is denied`` () =
    let pr = { Session = session "adv-2" (Some wealthCo) LocalPasskey 1.0; Role = Advisor }
    Assert.True(match decide' pr ViewAccount with Deny _ -> true | _ -> false)

[<Fact>]
let ``advisors cannot change delegation; partner admins manage users but not donor accounts`` () =
    Assert.True(match decide' (advisor LocalPasskey 1.0) ChangeDelegation with Deny _ -> true | _ -> false)
    let admin = { Session = session "padmin" (Some wealthCo) (PartnerFederated(wealthCo, set [ "hwk" ])) 1.0; Role = PartnerAdmin }
    Assert.Equal(Allow, decide' admin ManagePartnerUsers)
    Assert.True(match decide' admin ViewAccount with Deny _ -> true | _ -> false)

[<Fact>]
let ``a SCIM-deprovisioned user is denied immediately`` () =
    let pr = { advisor LocalPasskey 1.0 with Session = { (session "adv-1" (Some wealthCo) LocalPasskey 1.0) with Active = false } }
    Assert.Equal(Deny "user deprovisioned", decide' pr ViewAccount)

[<Fact>]
let ``staff privileged operations need just-in-time privilege and fresh phishing-resistant MFA`` () =
    let staff jit meth age = { Session = session "s-1" None meth age; Role = SponsorStaff jit }
    Assert.True(match decide' (staff false LocalPasskey 1.0) StaffPrivilegedOperation with Deny _ -> true | _ -> false)
    Assert.True(match decide' (staff true LocalTotp 1.0) StaffPrivilegedOperation with StepUp _ -> true | _ -> false)
    Assert.Equal(Allow, decide' (staff true LocalPasskey 1.0) StaffPrivilegedOperation)

[<Fact>]
let ``partner machine clients need sender-constrained tokens, own-org accounts and the scope`` () =
    let c = { Client = ClientId "wealthco-orion-sync"; Org = wealthCo; MtlsBound = true; Scopes = set [ "positions:read" ] }
    Assert.Equal(Allow, decideMachine c acct "positions:read")
    Assert.True(match decideMachine { c with MtlsBound = false } acct "positions:read" with Deny _ -> true | _ -> false)
    Assert.True(match decideMachine c acct "grants:write" with Deny _ -> true | _ -> false)
    Assert.True(match decideMachine { c with Org = otherCo } acct "positions:read" with Deny _ -> true | _ -> false)

// "APIs for everything" (DD-019): coverage tests over the design CSVs
open Daf.Enterprise.Tests.Fixtures

[<Fact>]
let ``every capability has at least one API`` () =
    readCsv "04-enterprise-apis/capability-api-coverage.csv"
    |> List.iter (fun r -> Assert.False(System.String.IsNullOrWhiteSpace r.["apis_after"], r.["capability_id"]))

[<Fact>]
let ``every business event is published by some API`` () =
    let published = readCsv "04-enterprise-apis/api-catalog.csv" |> List.map (fun r -> r.["events_published"]) |> String.concat " "
    readCsv "06-data-and-knowledge/events.csv"
    |> List.iter (fun r -> Assert.True(published.Contains r.["event_type"], r.["event_type"]))

[<Fact>]
let ``every API declares an exposure tier and an authorization boundary`` () =
    readCsv "04-enterprise-apis/api-catalog.csv"
    |> List.iter (fun r ->
        Assert.False(System.String.IsNullOrWhiteSpace r.["exposure"], r.["api_id"])
        Assert.False(System.String.IsNullOrWhiteSpace r.["authorization_boundary"], r.["api_id"]))

[<Fact>]
let ``every legal requirement that applies to the sponsor maps to existing controls (A1)`` () =
    let controls = readCsv "08-governance-and-compliance/controls.csv" |> List.map (fun r -> r.["control_id"]) |> set
    readCsv "08-governance-and-compliance/reg-control-mapping.csv"
    |> List.iter (fun r ->
        Assert.NotEqual<string>("GAP", r.["status"])
        if r.["status"] = "mapped" then
            r.["control_ids"].Split(';') |> Array.iter (fun c -> Assert.True(controls.Contains c, r.["req_id"] + " -> " + c)))
