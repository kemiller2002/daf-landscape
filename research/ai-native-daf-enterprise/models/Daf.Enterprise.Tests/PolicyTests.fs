module Daf.Enterprise.Tests.PolicyTests

open Xunit
open Daf.Enterprise.Domain
open Daf.Enterprise.Policy
open Daf.Enterprise.Tests.Fixtures

let isApproveByRule = function Approve(RuleActor _, _) -> true | _ -> false
let referredFor code = function Refer(fs, _) -> fs |> List.exists (fun f -> f.Code = code) | _ -> false

[<Fact>]
let ``routine grant to listed public charity under threshold is approved by rule with no human`` () =
    Assert.True(decide policy (context (recommendation 5000m "k1")) |> isApproveByRule)

[<Fact>]
let ``revoked recipient is denied`` () =
    let ctx = { context (recommendation 5000m "k") with Eligibility = Some { eligible with Revoked = true } }
    match decide policy ctx with
    | Deny _ -> ()
    | d -> failwithf "expected deny, got %A" d

[<Fact>]
let ``stale eligibility data blocks the deterministic path`` () =
    let ctx = { context (recommendation 5000m "k") with Eligibility = Some { eligible with Stamp = stamp 60.0 } }
    Assert.True(decide policy ctx |> referredFor StaleEligibilityData)

[<Fact>]
let ``missing eligibility data is referred, never approved`` () =
    Assert.True(decide policy { context (recommendation 5000m "k") with Eligibility = None } |> referredFor StaleEligibilityData)

[<Fact>]
let ``OFAC hit is referred for the sanctions officer`` () =
    let ctx = { context (recommendation 5000m "k") with Eligibility = Some { eligible with OfacListed = true } }
    Assert.True(decide policy ctx |> referredFor SanctionsPotentialMatch)

[<Theory>]
[<InlineData("pf")>]
[<InlineData("t3")>]
[<InlineData("nc")>]
let ``non-public-charity recipients require expenditure responsibility`` (kind: string) =
    let cls = match kind with "pf" -> PrivateFoundation | "t3" -> Type3NonFunctionallyIntegrated | _ -> NonCharity
    let ctx = { context (recommendation 5000m "k") with Eligibility = Some { eligible with Class = cls } }
    Assert.True(decide policy ctx |> referredFor RequiresExpenditureResponsibility)

[<Fact>]
let ``foreign recipient is referred`` () =
    let ctx = { context (recommendation 5000m "k") with Eligibility = Some { eligible with Class = ForeignOrganization } }
    Assert.True(decide policy ctx |> referredFor ForeignRecipient)

[<Fact>]
let ``amount above auto limit is referred`` () =
    Assert.True(decide policy (context (recommendation 250001m "k")) |> referredFor AmountAboveAutoThreshold)

[<Fact>]
let ``recipient related to an account party is referred for benefit review`` () =
    let ctx = { context (recommendation 5000m "k") with Recipient = { recipient with RelatedPartyIds = [ donor ] } }
    Assert.True(decide policy ctx |> referredFor PossibleRelatedPartyRecipient)

[<Fact>]
let ``new organization and fiscal sponsor are sponsor-policy referrals`` () =
    let ctxNew = { context (recommendation 5000m "k") with Eligibility = Some { eligible with RulingYear = Some 2026 } }
    let ctxFs = { context (recommendation 5000m "k") with Recipient = { recipient with IsFiscalSponsor = true } }
    Assert.True(decide policy ctxNew |> referredFor NewOrganization)
    Assert.True(decide policy ctxFs |> referredFor FiscalSponsorIntermediary)

[<Fact>]
let ``an uncleared agent flag forces referral; agents add flags but never clear`` () =
    let agentFlag = { Code = PossibleProhibitedBenefit; RaisedBy = AgentActor("benefit-risk", "v1"); Detail = "gala tickets"; Clearance = None }
    Assert.True(decide policy { context (recommendation 5000m "k") with AgentFlags = [ agentFlag ] } |> referredFor PossibleProhibitedBenefit)

[<Fact>]
let ``discretionary board hold is referred`` () =
    let p = { policy with DiscretionaryHolds = Set.singleton recipientId }
    Assert.True(decide p (context (recommendation 5000m "k")) |> referredFor DiscretionaryPolicyHold)

[<Fact>]
let ``non-positive amounts are denied`` () =
    match decide policy (context (recommendation 0m "k")) with
    | Deny _ -> ()
    | d -> failwithf "expected deny, got %A" d

[<Fact>]
let ``decisions are deterministic for the same inputs and policy version`` () =
    let r = recommendation 5000m "k"
    Assert.Equal(decide policy (context r), decide policy (context r))

// ---------- human authority ----------
let flagOf code = { Code = code; RaisedBy = RuleActor(policy.Ref, "x"); Detail = ""; Clearance = None }

[<Fact>]
let ``grants compliance cannot clear a sanctions flag`` () =
    match humanApprove complianceOfficer (Set.singleton donor) 5000m [ flagOf SanctionsPotentialMatch ] with
    | Error(NotAuthorizedForFlag SanctionsPotentialMatch) -> ()
    | r -> failwithf "unexpected %A" r

[<Fact>]
let ``sanctions officer can clear a sanctions flag and the clearance names the person`` () =
    match humanApprove sanctionsOfficer (Set.singleton donor) 5000m [ flagOf SanctionsPotentialMatch ] with
    | Ok(flags, Approve(PersonActor("S-sanctions-1", _), _)) ->
        Assert.All(flags, fun f -> Assert.Equal(Some(ClearedByPerson("S-sanctions-1", "DOA-2026-SO-1")), f.Clearance))
    | r -> failwithf "unexpected %A" r

[<Fact>]
let ``approver above authority limit fails`` () =
    match humanApprove complianceOfficer (Set.singleton donor) 2000000m [ flagOf ForeignRecipient ] with
    | Error(AboveAuthorityLimit _) -> ()
    | r -> failwithf "unexpected %A" r

[<Fact>]
let ``approver related to the account cannot decide (segregation of duties)`` () =
    let conflicted = { complianceOfficer with RelatedParties = Set.singleton donor }
    match humanApprove conflicted (Set.singleton donor) 5000m [ flagOf ForeignRecipient ] with
    | Error ConflictOfInterest -> ()
    | r -> failwithf "unexpected %A" r

[<Fact>]
let ``canApprove is false for agents and external systems`` () =
    Assert.False(canApprove (AgentActor("any", "v1")))
    Assert.False(canApprove (ExternalActor "custodian"))
    Assert.True(canApprove (RuleActor(policy.Ref, "r")))
    Assert.True(canApprove (PersonActor("p", "a")))
