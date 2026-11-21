/// End-to-end reference journey (addendum §24) as executable acceptance tests.
module Daf.Enterprise.Tests.JourneyTests

open System
open Xunit
open Daf.Enterprise.Domain
open Daf.Enterprise.Policy
open Daf.Enterprise.Ledger
open Daf.Enterprise.Journey
open Daf.Enterprise.Tests.Fixtures

let limits = { PerRecipientDailyCap = 1000000m; DualControlAbove = 100000m }
let profile = { Recipient = recipientId; Rail = "ACH-CCD+"; AccountToken = "tok_1"; Verified = true; CoolingOffUntil = None }
let ctxFn = fun r -> context r

let onboardAndFund amount =
    [ VerifyIdentity donor
      OpenAccount(account, donor, "agreement-v7")
      DeclareIntent(account, "CI-001", amount)
      SettleContribution("CI-001", amount, "CUST-998", now) ]

let ok = function
    | Ok x -> x
    | Error(e, _) -> failwithf "rejected: %A" e

[<Fact>]
let ``full journey: onboarding to reconciliation and reporting with no human touch for a routine grant`` () =
    let gid = GrantId "G-1"
    let pid = PaymentId "PAY-1"
    let cmds =
        onboardAndFund 100000m
        @ [ SubmitRecommendation(gid, recommendation 5000m "rec-1")
            Evaluate(gid, policy, ctxFn)
            ReleasePayment(gid, pid, profile, limits, now, None)
            SettlePayment(pid, "ACH-TRACE-1") ]
    let (s, events) = run empty cmds |> ok
    // state
    Assert.Equal(Paid(pid, "ACH-TRACE-1"), s.Grants.[gid].State)
    Assert.Equal(95000m, available s account)
    Assert.True(identityHolds s.Journal)
    Assert.True(s.Journal |> List.forall isBalanced)
    // no exception case was opened, the approval was by rule
    Assert.DoesNotContain(events, fun e -> match e with ExceptionCaseOpened _ -> true | _ -> false)
    Assert.Contains(events, fun e -> match e with GrantApproved(_, RuleActor _) -> true | _ -> false)
    // acknowledgment carries the exclusive legal control statement (§170(f)(18))
    let ack = events |> List.pick (function AcknowledgmentIssued(_, _, t) -> Some t | _ -> None)
    Assert.Contains("exclusive legal control", ack)
    // remittance carries the grant id
    let instr = events |> List.pick (function PaymentInstructed i -> Some i | _ -> None)
    Assert.True instr.GrantIdInRemittance
    // reconciliation: clean statement -> no breaks; tampered statement -> breaks
    Assert.Empty(reconcile s [ { Reference = instr.IdempotencyKey; Amount = 5000m } ])
    Assert.Equal(1, (reconcile s [ { Reference = instr.IdempotencyKey; Amount = 4999m } ]).Length)
    Assert.Equal(2, (reconcile s [ { Reference = "unknown"; Amount = 5000m } ]).Length)
    // reporting is derived from the ledger
    let d = scheduleD s events
    Assert.Equal({ Accounts = 1; Contributions = 100000m; GrantsPaid = 5000m; YearEndFundBalances = 95000m }, d)
    // evidence recorded for contribution match, decision and payment gate
    let controls = events |> List.choose (function EvidenceRecorded e -> Some e.Control | _ -> None) |> set
    Assert.Equal<Set<string>>(set [ "CTL-contribution-three-way-match"; "CTL-grant-decision-record"; "CTL-payment-gate" ], controls)

[<Fact>]
let ``flagged grant waits for a human; payment gate refuses until approved`` () =
    let gid = GrantId "G-2"
    let (s, events) =
        run empty (onboardAndFund 100000m
                   @ [ SubmitRecommendation(gid, recommendation 5000m "rec-2")
                       ApplyAgentOutput(gid, RaiseFlag { Code = PossibleProhibitedBenefit; RaisedBy = RuleActor(policy.Ref, "spoof"); Detail = "pledge language"; Clearance = Some(ClearedByRule(policy.Ref, "spoof")) }, "benefit-risk")
                       Evaluate(gid, policy, ctxFn) ]) |> ok
    // the agent's attempt to pre-clear and to impersonate a rule was neutralised
    let flagged = s.Grants.[gid].Flags |> List.find (fun f -> f.Code = PossibleProhibitedBenefit)
    Assert.Equal(AgentActor("benefit-risk", "v1"), flagged.RaisedBy)
    Assert.Equal(None, flagged.Clearance)
    Assert.Contains(events, fun e -> match e with ExceptionCaseOpened _ -> true | _ -> false)
    match handle s (ReleasePayment(gid, PaymentId "PAY-2", profile, limits, now, None)) with
    | Error(PaymentGateFailed reasons) -> Assert.Contains(reasons, fun r -> r.StartsWith "grant not approved")
    | r -> failwithf "unexpected %A" r
    // the human decides, then payment proceeds
    let (s2, ev2) = handle s (HumanDecide(gid, complianceOfficer)) |> Result.defaultWith (fun e -> failwithf "%A" e)
    Assert.Contains(ev2, fun e -> match e with ExceptionCaseResolved(_, PersonActor _) -> true | _ -> false)
    Assert.True(Result.isOk (handle s2 (ReleasePayment(gid, PaymentId "PAY-2", profile, limits, now, None))))

[<Fact>]
let ``an agent actor can never approve a grant`` () =
    let gid = GrantId "G-3"
    let (s, _) = run empty (onboardAndFund 10000m @ [ SubmitRecommendation(gid, recommendation 500m "rec-3") ]) |> ok
    match handle s (AttemptApproveAs(gid, AgentActor("rogue", "v9"))) with
    | Error(AgentCannotAuthorize _) -> ()
    | r -> failwithf "unexpected %A" r

[<Fact>]
let ``agent proposals change no authoritative state`` () =
    let gid = GrantId "G-4"
    let (s, _) = run empty (onboardAndFund 10000m @ [ SubmitRecommendation(gid, recommendation 500m "rec-4") ]) |> ok
    let (s2, evs) = handle s (ApplyAgentOutput(gid, DraftDossier("G-4", "summary"), "dossier")) |> Result.defaultWith (fun e -> failwithf "%A" e)
    Assert.Equal(s, s2)
    Assert.Empty evs

[<Fact>]
let ``payment gate: cooling-off, unverified payee, wrong payee, dual control, daily cap`` () =
    let gid = GrantId "G-5"
    let (s, _) =
        run empty (onboardAndFund 1000000m @ [ SubmitRecommendation(gid, recommendation 200000m "rec-5"); Evaluate(gid, policy, ctxFn) ]) |> ok
    let fails p lim second =
        match handle s (ReleasePayment(gid, PaymentId "P", p, lim, now, second)) with
        | Error(PaymentGateFailed r) -> r
        | _ -> []
    Assert.Contains("payee profile change in cooling-off", fails { profile with CoolingOffUntil = Some(now.AddDays 2.0) } limits (Some "S-2"))
    Assert.Contains("payee profile not verified", fails { profile with Verified = false } limits (Some "S-2"))
    Assert.Contains("payee profile is for a different recipient", fails { profile with Recipient = RecipientId "R-other" } limits (Some "S-2"))
    Assert.Contains("dual control required", fails profile limits None)
    Assert.Contains("per-recipient daily cap exceeded", fails profile { limits with PerRecipientDailyCap = 100000m } (Some "S-2"))
    Assert.True(Result.isOk (handle s (ReleasePayment(gid, PaymentId "P", profile, limits, now, Some "S-2"))))

[<Fact>]
let ``duplicate recommendation and duplicate custodian settlement are rejected (idempotency)`` () =
    let (s, _) = run empty (onboardAndFund 10000m @ [ SubmitRecommendation(GrantId "G-6", recommendation 100m "same-key") ]) |> ok
    match handle s (SubmitRecommendation(GrantId "G-7", recommendation 100m "same-key")) with
    | Error(DuplicateIdempotencyKey _) -> ()
    | r -> failwithf "unexpected %A" r
    let s2 = { s with Intents = s.Intents.Add("CI-002", (account, 5m)) }
    match handle s2 (SettleContribution("CI-002", 5m, "CUST-998", now)) with
    | Error(DuplicateIdempotencyKey _) -> ()
    | r -> failwithf "unexpected %A" r

[<Fact>]
let ``unprivileged party cannot recommend; unverified donor cannot open an account`` () =
    let (s, _) = run empty (onboardAndFund 10000m) |> ok
    let stranger = { recommendation 100m "x" with RequestedBy = PartyId "P-stranger" }
    Assert.True(match handle s (SubmitRecommendation(GrantId "G-8", stranger)) with Error(NotPrivileged _) -> true | _ -> false)
    Assert.True(match handle empty (OpenAccount(account, donor, "v")) with Error(IdentityNotVerified _) -> true | _ -> false)

[<Fact>]
let ``orphan receipt goes to suspense and raises a break, never guessed into an account`` () =
    let (s, evs) = run empty [ VerifyIdentity donor; OpenAccount(account, donor, "v"); SettleContribution("NO-INTENT", 700m, "CUST-1", now) ] |> ok
    Assert.Equal(0m, available s account)
    Assert.Equal(700m, balance s.Journal Suspense)
    Assert.Contains(evs, fun e -> match e with ReconciliationBreakDetected _ -> true | _ -> false)
    Assert.True(identityHolds s.Journal)

[<Fact>]
let ``returned payment restores the fund balance and keeps the ledger balanced`` () =
    let gid = GrantId "G-9"
    let pid = PaymentId "PAY-9"
    let (s, _) =
        run empty (onboardAndFund 10000m
                   @ [ SubmitRecommendation(gid, recommendation 1000m "rec-9"); Evaluate(gid, policy, ctxFn)
                       ReleasePayment(gid, pid, profile, limits, now, None); ReturnPayment(pid, "R03") ]) |> ok
    Assert.Equal(Returned(pid, "R03"), s.Grants.[gid].State)
    Assert.Equal(10000m, available s account)
    Assert.Equal(0m, balance s.Journal CashInTransit)
    Assert.True(identityHolds s.Journal)

[<Fact>]
let ``insufficient balance declines rather than overdrawing`` () =
    let gid = GrantId "G-10"
    let (s, _) = run empty (onboardAndFund 1000m @ [ SubmitRecommendation(gid, recommendation 5000m "rec-10"); Evaluate(gid, policy, ctxFn) ]) |> ok
    Assert.Equal(Declined "insufficient fund balance", s.Grants.[gid].State)
    Assert.Equal(1000m, available s account)

[<Fact>]
let ``high-volume burst: 2,000 routine grants process without a human and the ledger stays consistent`` () =
    let n = 2000
    let grants =
        [ for i in 1..n ->
            let gid = GrantId $"B-{i}"
            [ SubmitRecommendation(gid, recommendation 50m $"burst-{i}"); Evaluate(gid, policy, ctxFn) ] ]
        |> List.concat
    let (s, events) = run empty (onboardAndFund 200000m @ grants) |> ok
    let approved = events |> List.filter (function GrantApproved(_, RuleActor _) -> true | _ -> false) |> List.length
    Assert.Equal(n, approved)
    Assert.Equal(100000m, available s account)
    Assert.True(identityHolds s.Journal)
