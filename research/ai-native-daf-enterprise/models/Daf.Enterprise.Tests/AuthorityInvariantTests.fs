/// Authority invariants INV-A1..INV-A8 from 05-agent-architecture/authority-boundaries.md,
/// plus the eligibility-change hold from the event catalog (§4 rule 5).
module Daf.Enterprise.Tests.AuthorityInvariantTests

open Xunit
open Daf.Enterprise.Domain
open Daf.Enterprise.Policy
open Daf.Enterprise.Ledger
open Daf.Enterprise.Journey
open Daf.Enterprise.Tests.Fixtures
open Daf.Enterprise.Tests.JourneyTests

let authoritativeActors events =
    events |> List.choose (function
        | GrantApproved(_, a) | ExceptionCaseResolved(_, a) -> Some a
        | _ -> None)

/// A small corpus of journeys covering routine, referred, human-approved, returned and held paths.
let corpus () =
    let agentFlag = RaiseFlag { Code = PossibleProhibitedBenefit; RaisedBy = AgentActor("x", "1"); Detail = ""; Clearance = None }
    [ onboardAndFund 100000m @ [ SubmitRecommendation(GrantId "C1", recommendation 100m "c1"); Evaluate(GrantId "C1", policy, ctxFn)
                                 ReleasePayment(GrantId "C1", PaymentId "CP1", profile, limits, now, None); SettlePayment(PaymentId "CP1", "t") ]
      onboardAndFund 100000m @ [ SubmitRecommendation(GrantId "C2", recommendation 100m "c2"); ApplyAgentOutput(GrantId "C2", agentFlag, "benefit-risk")
                                 Evaluate(GrantId "C2", policy, ctxFn); HumanDecide(GrantId "C2", complianceOfficer)
                                 ReleasePayment(GrantId "C2", PaymentId "CP2", profile, limits, now, None); ReturnPayment(PaymentId "CP2", "R01") ]
      onboardAndFund 100000m @ [ SubmitRecommendation(GrantId "C3", recommendation 300000m "c3"); Evaluate(GrantId "C3", policy, ctxFn) ] ]
    |> List.map (fun cmds -> match run empty cmds with Ok(s, e) -> (s, e) | Error(err, _) -> failwithf "%A" err)

[<Fact>]
let ``INV-A1/A2: every approving or flag-clearing actor is a rule or a person`` () =
    for (s, events) in corpus () do
        authoritativeActors events |> List.iter (fun a -> Assert.True(canApprove a, $"%A{a}"))
        s.Grants |> Map.iter (fun _ g ->
            g.Flags |> List.iter (fun f ->
                match f.Clearance with
                | None | Some(ClearedByRule _) | Some(ClearedByPerson _) -> ()))  // no agent constructor exists

[<Fact>]
let ``INV-A3: no PaymentInstructed without a prior GrantApproved for that grant`` () =
    for (_, events) in corpus () do
        events |> List.iteri (fun i e ->
            match e with
            | PaymentInstructed instr ->
                let prior = events |> List.take i
                Assert.Contains(prior, fun p -> match p with GrantApproved(g, _) -> g = instr.Grant | _ -> false)
            | _ -> ())

[<Fact>]
let ``INV-A4: no rule approval while a flag is open`` () =
    for (s, events) in corpus () do
        events |> List.iter (function
            | GrantApproved(gid, RuleActor _) ->
                let opened = s.Grants.[gid].Flags |> List.filter (isCleared >> not)
                Assert.Empty opened
            | _ -> ())

[<Fact>]
let ``INV-A5: agent tool scopes contain no money, ledger, approval or clearance capability`` () =
    // Exhaustive match: adding a new scope case forces this test (and a review) to change.
    let describe = function
        | ReadScope _ -> "read" | ProposeScope -> "propose" | RaiseFlagScope -> "flag"
        | OpenCaseScope -> "case" | DraftScope -> "draft" | SendTemplatedScope _ -> "send"
    let all = [ ReadScope "grants"; ProposeScope; RaiseFlagScope; OpenCaseScope; DraftScope; SendTemplatedScope "t" ]
    Assert.Equal<string list>([ "read"; "propose"; "flag"; "case"; "draft"; "send" ], all |> List.map describe)

[<Fact>]
let ``INV-A6: agent-originated request above confirm_above waits for the delegating donor`` () =
    let agentRec = { recommendation 5000m "agent-1" with ViaAgent = Some "donor-assistant" }
    let (s, evs) =
        run empty (onboardAndFund 100000m
                   @ [ DelegateToAgent(account, donor, "donor-assistant", 1000m)
                       SubmitRecommendation(GrantId "AG1", agentRec) ]) |> function Ok x -> x | Error(e, _) -> failwithf "%A" e
    Assert.Equal(AwaitingDonorConfirmation, s.Grants.[GrantId "AG1"].State)
    Assert.Contains(evs, fun e -> match e with DonorConfirmationRequested _ -> true | _ -> false)
    // cannot be evaluated, and cannot be confirmed by anyone but the donor
    Assert.True(Result.isError (handle s (Evaluate(GrantId "AG1", policy, ctxFn))))
    Assert.True(Result.isError (handle s (ConfirmRecommendation(GrantId "AG1", PartyId "P-advisor"))))
    let (s2, _) = handle s (ConfirmRecommendation(GrantId "AG1", donor)) |> Result.defaultWith (fun e -> failwithf "%A" e)
    Assert.Equal(Submitted, s2.Grants.[GrantId "AG1"].State)

[<Fact>]
let ``INV-A6: an undelegated agent cannot submit, and below the cap no confirmation is needed`` () =
    let (s, _) = run empty (onboardAndFund 100000m @ [ DelegateToAgent(account, donor, "donor-assistant", 1000m) ]) |> function Ok x -> x | Error(e, _) -> failwithf "%A" e
    Assert.True(Result.isError (handle s (SubmitRecommendation(GrantId "U", { recommendation 10m "u" with ViaAgent = Some "unknown-agent" }))))
    match handle s (SubmitRecommendation(GrantId "B", { recommendation 500m "b" with ViaAgent = Some "donor-assistant" })) with
    | Ok(s2, _) -> Assert.Equal(Submitted, s2.Grants.[GrantId "B"].State)
    | Error e -> failwithf "%A" e
    // only the donor may delegate
    Assert.True(Result.isError (handle s (DelegateToAgent(account, PartyId "P-advisor", "x", 1m))))

[<Fact>]
let ``INV-A7: a related staff member can neither approve nor decline`` () =
    let conflicted = { complianceOfficer with RelatedParties = Set.singleton donor }
    let (s, _) = run empty (onboardAndFund 100000m @ [ SubmitRecommendation(GrantId "R1", recommendation 300000m "r1"); Evaluate(GrantId "R1", policy, ctxFn) ]) |> function Ok x -> x | Error(e, _) -> failwithf "%A" e
    Assert.True(Result.isError (handle s (HumanDecide(GrantId "R1", conflicted))))
    Assert.True(Result.isError (handle s (HumanDecline(GrantId "R1", conflicted, "x"))))

[<Fact>]
let ``INV-A8: chains deeper than 8 without a checkpoint are quarantined`` () =
    let agent = AgentActor("a", "1")
    let rule = RuleActor(policy.Ref, "r")
    Assert.False(mustQuarantine 8 (List.replicate 8 agent))
    Assert.True(mustQuarantine 8 (List.replicate 9 agent))
    Assert.False(mustQuarantine 8 (List.replicate 5 agent @ [ rule ] @ List.replicate 5 agent))

[<Fact>]
let ``eligibility change holds approved-unreleased grants, reverses the commitment, and never releases`` () =
    let gid = GrantId "E1"
    let (s, _) = run empty (onboardAndFund 10000m @ [ SubmitRecommendation(gid, recommendation 1000m "e1"); Evaluate(gid, policy, ctxFn) ]) |> function Ok x -> x | Error(e, _) -> failwithf "%A" e
    Assert.Equal(9000m, available s account)
    let (s2, evs) = handle s (ChangeEligibility { eligible with Revoked = true; Stamp = stamp 0.0 }) |> Result.defaultWith (fun e -> failwithf "%A" e)
    match s2.Grants.[gid].State with
    | AwaitingHumanDecision _ -> ()
    | st -> failwithf "expected hold, got %A" st
    Assert.Equal(10000m, available s2 account)
    Assert.True(identityHolds s2.Journal)
    Assert.Contains(evs, fun e -> match e with ExceptionCaseOpened _ -> true | _ -> false)
    // the payment gate refuses the held grant
    Assert.True(Result.isError (handle s2 (ReleasePayment(gid, PaymentId "EP", profile, limits, now, None))))
    // a person declines it
    let (s3, _) = handle s2 (HumanDecline(gid, complianceOfficer, "recipient revoked")) |> Result.defaultWith (fun e -> failwithf "%A" e)
    Assert.Equal(Declined "recipient revoked", s3.Grants.[gid].State)

[<Fact>]
let ``eligibility change after release opens a post-payment review instead of pretending to recall`` () =
    let gid = GrantId "E2"
    let (s, _) = run empty (onboardAndFund 10000m @ [ SubmitRecommendation(gid, recommendation 1000m "e2"); Evaluate(gid, policy, ctxFn); ReleasePayment(gid, PaymentId "EP2", profile, limits, now, None) ]) |> function Ok x -> x | Error(e, _) -> failwithf "%A" e
    let (_, evs) = handle s (ChangeEligibility { eligible with OfacListed = true }) |> Result.defaultWith (fun e -> failwithf "%A" e)
    Assert.Contains(evs, fun e -> match e with PostPaymentReviewOpened(g, _) -> g = gid | _ -> false)
