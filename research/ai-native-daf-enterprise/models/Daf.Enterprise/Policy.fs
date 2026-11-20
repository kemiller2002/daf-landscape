/// Grant decisioning as policy-as-code (DD-004, DD-011, DD-012).
/// Pure functions: the same inputs and policy version always give the same decision.
module Daf.Enterprise.Policy

open System
open Daf.Enterprise.Domain

/// A versioned, human-approved policy. Thresholds are governed parameters (DEC-058).
type GrantPolicy =
    { Ref: PolicyRef
      AutoApproveLimit: Usd                 // above this a person must decide
      EligibilityFreshness: TimeSpan        // older data blocks the deterministic path
      NewOrgYears: int                      // sponsor risk policy, not law
      DiscretionaryHolds: Set<RecipientId>  // board-approved holds (ACT-029)
      ApprovedBy: string }                  // approval record reference

type DecisionContext =
    { Now: DateTime
      Recommendation: Recommendation
      Recipient: Recipient
      Eligibility: EligibilitySnapshot option
      AccountParties: Set<PartyId>          // donors/advisors/successors on the account and their declared relations
      AgentFlags: Flag list }               // Category 2 output: flags only

let private flag code detail (policy: GrantPolicy) ruleId =
    { Code = code
      RaisedBy = RuleActor(policy.Ref, ruleId)
      Detail = detail
      Clearance = None }

/// Deterministic checks. Each returns at most one hard outcome or a list of flags.
type private Check =
    | Pass
    | HardDeny of string
    | Flags of Flag list

let private checks (p: GrantPolicy) (c: DecisionContext) : Check list =
    let r = c.Recommendation
    let eligibility =
        match c.Eligibility with
        | None -> Flags [ flag StaleEligibilityData "no eligibility snapshot" p "R-ELIG-01" ]
        | Some e when c.Now - e.Stamp.RetrievedAt > p.EligibilityFreshness ->
            Flags [ flag StaleEligibilityData $"snapshot {e.Stamp.SourceVersion} older than freshness SLO" p "R-ELIG-02" ]
        | Some e when e.Revoked -> HardDeny "recipient exemption revoked (IRS auto-revocation list)"
        | Some e ->
            match e.Class with
            | PublicCharity170b1A -> Pass
            | ForeignOrganization -> Flags [ flag ForeignRecipient "foreign recipient: equivalency determination or expenditure responsibility" p "R-ELIG-03" ]
            | PrivateFoundation
            | Type3NonFunctionallyIntegrated
            | Other501c3NotPublicCharity
            | NonCharity -> Flags [ flag RequiresExpenditureResponsibility "§4966(c)(1)(B): expenditure responsibility required" p "R-ELIG-04" ]
    let sanctions =
        match c.Eligibility with
        | Some e when e.OfacListed -> Flags [ flag SanctionsPotentialMatch "OFAC list hit: only the sanctions officer may decide" p "R-SANC-01" ]
        | _ -> Pass
    let newOrg =
        match c.Eligibility |> Option.bind (fun e -> e.RulingYear) with
        | Some y when c.Now.Year - y < p.NewOrgYears -> Flags [ flag NewOrganization $"ruling year {y}" p "R-RISK-01" ]
        | _ -> Pass
    let fiscal =
        if c.Recipient.IsFiscalSponsor then Flags [ flag FiscalSponsorIntermediary "fiscal sponsor: confirm charitable purpose and no earmark to a non-charity" p "R-RISK-02" ]
        else Pass
    let related =
        let overlap = Set.intersect (Set.ofList c.Recipient.RelatedPartyIds) c.AccountParties
        if Set.isEmpty overlap then Pass
        else Flags [ flag PossibleRelatedPartyRecipient "recipient related to account party: §4967/§4958 review" p "R-BEN-01" ]
    let amount =
        if r.Amount > p.AutoApproveLimit then Flags [ flag AmountAboveAutoThreshold $"amount {r.Amount} > {p.AutoApproveLimit}" p "R-AMT-01" ]
        else Pass
    let hold =
        if p.DiscretionaryHolds.Contains r.Recipient then Flags [ flag DiscretionaryPolicyHold "board-approved discretionary hold" p "R-HOLD-01" ]
        else Pass
    let agentFlags =
        match c.AgentFlags |> List.filter (isCleared >> not) with
        | [] -> Pass
        | fs -> Flags fs
    [ eligibility; sanctions; newOrg; fiscal; related; amount; hold; agentFlags ]

/// Evaluate a recommendation. Invalid input is denied before any check.
let decide (p: GrantPolicy) (c: DecisionContext) : Decision =
    if c.Recommendation.Amount <= 0m then Deny("amount must be positive", p.Ref)
    else
        let results = checks p c
        match results |> List.tryPick (function HardDeny reason -> Some reason | _ -> None) with
        | Some reason -> Deny(reason, p.Ref)
        | None ->
            match results |> List.collect (function Flags fs -> fs | _ -> []) with
            | [] -> Approve(RuleActor(p.Ref, "R-ROUTINE"), p.Ref)
            | fs -> Refer(fs, p.Ref)

// ---------- human authority ----------
type Role =
    | GrantsCompliance
    | SanctionsOfficer
    | Controller
    | ProgramOfficer

type Approver =
    { PersonId: string
      Roles: Set<Role>
      AuthorityLimit: Usd
      RelatedParties: Set<PartyId>   // parties this staff member is related to
      AuthorityRef: string }

type HumanDecisionError =
    | NotAuthorizedForFlag of FlagCode
    | AboveAuthorityLimit of Usd
    | ConflictOfInterest
    | NothingToDecide

/// Which role may clear which flag.
let requiredRole =
    function
    | SanctionsPotentialMatch -> SanctionsOfficer
    | PayeeProfileInCoolingOff -> Controller
    | DiscretionaryPolicyHold -> ProgramOfficer
    | _ -> GrantsCompliance

/// A person clears every outstanding flag and approves, or the attempt fails with a reason.
/// The person cannot approve beyond their limit, cannot clear flags outside their role,
/// and cannot act on an account they are related to (segregation of duties).
let humanApprove (approver: Approver) (accountParties: Set<PartyId>) (amount: Usd) (flags: Flag list)
    : Result<Flag list * Decision, HumanDecisionError> =
    let open' = flags |> List.filter (isCleared >> not)
    if List.isEmpty open' then Error NothingToDecide
    elif not (Set.isEmpty (Set.intersect approver.RelatedParties accountParties)) then Error ConflictOfInterest
    elif amount > approver.AuthorityLimit then Error(AboveAuthorityLimit approver.AuthorityLimit)
    else
        match open' |> List.tryFind (fun f -> not (approver.Roles.Contains(requiredRole f.Code))) with
        | Some f -> Error(NotAuthorizedForFlag f.Code)
        | None ->
            let cleared =
                flags |> List.map (fun f ->
                    if isCleared f then f
                    else { f with Clearance = Some(ClearedByPerson(approver.PersonId, approver.AuthorityRef)) })
            let actor = PersonActor(approver.PersonId, approver.AuthorityRef)
            Ok(cleared, Approve(actor, { PolicyId = "human-authority"; Version = 1 }))
