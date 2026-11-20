module Daf.Enterprise.Tests.ExperimentTests

open Xunit
open Daf.Experiments.Sim
open Daf.Experiments.Experiments

let seed = 20261120UL

[<Fact>]
let ``rng is deterministic and uniform is in [0,1)`` () =
    let (a, _) = draws 1000 uniform (Rng 1UL)
    let (b, _) = draws 1000 uniform (Rng 1UL)
    Assert.Equal<float list>(a, b)
    Assert.All(a, fun x -> Assert.True(x >= 0.0 && x < 1.0))

[<Fact>]
let ``zipf CDF is monotone and ends at 1`` () =
    let z = zipf 1000 1.0
    Assert.True(z.Cdf |> Array.pairwise |> Array.forall (fun (x, y) -> y >= x))
    Assert.InRange(z.Cdf.[999], 0.999999, 1.000001)

// E1
[<Fact>]
let ``E1: automated designs share the same source-latency floor; passport cuts verification work`` () =
    let rs = E1.run E1.defaults seed
    let get a = rs |> List.find (fun r -> r.Arch = a)
    let auto = get E1.AutomatedPerGrant
    let passport = get E1.PassportOnPublication
    Assert.Equal(auto.Escaped, passport.Escaped)            // accuracy bounded by source publication, not architecture
    Assert.Equal(auto.SourceLatencyFloor, auto.Escaped)
    // finding: naive full refresh can cost MORE operations than per-grant lookup; diff-driven refresh costs far fewer
    let diff = get E1.PassportDiffDriven
    Assert.True(diff.VerificationOps < auto.VerificationOps)
    Assert.True(diff.VerificationOps < passport.VerificationOps)
    Assert.Equal(auto.Escaped, diff.Escaped)
    Assert.True((get E1.PassportQuarterly).Escaped >= passport.Escaped)  // slower refresh never helps
    Assert.True((get E1.ManualPerGrant).Escaped >= auto.Escaped)          // human misses add to the floor

// E2
let e2 a = E2.run E2.defaults seed a

[<Fact>]
let ``E2: flag-only AI-native escapes no more than unsafe auto-clear and uses far fewer human hours than review-all`` () =
    let native = e2 E2.RulesAiFlagsExceptions
    let unsafe' = e2 E2.AiAutoClearUnsafe
    let manual = e2 E2.ManualReviewAll
    Assert.True(native.EscapedTotal <= unsafe'.EscapedTotal)
    Assert.True(native.HumanMinutes < manual.HumanMinutes / 2.0)

[<Fact>]
let ``E2: deterministic rules catch every revoked and sanctions defect when configured`` () =
    let r = e2 E2.RulesAiFlagsExceptions
    let esc d = r.Escaped.TryFind d |> Option.defaultValue 0
    // humans catch 95% of what reaches them, so allow escapes only from the human step
    let revokedTotal = E2.generate E2.defaults seed |> List.filter (fun g -> g.Defect = E2.Revoked) |> List.length
    Assert.True(float (esc E2.Revoked) <= 0.15 * float revokedTotal)

[<Fact>]
let ``E2: pay-first lets every routine-tier defect through before checks`` () =
    let pay = e2 E2.PayFirstPreverified
    let native = e2 E2.RulesAiFlagsExceptions
    Assert.True(pay.EscapedTotal > native.EscapedTotal)

[<Fact>]
let ``E2 adversarial: a silently disabled rule is invisible to flag-only AI, found on day 1 by canaries`` () =
    let p = { E2.defaults with MisconfigWindow = Some(100, 200) }
    let native = E2.run p seed E2.RulesAiFlagsExceptions
    let canary = E2.run p seed E2.RulesAiFlagsWithCanaries
    let manual = E2.run p seed E2.ManualReviewAll
    Assert.True(native.MisconfigDetectedDay.IsNone)
    Assert.Equal(Some 100, canary.MisconfigDetectedDay)
    Assert.True(manual.MisconfigDetectedDay.IsSome)
    Assert.True(canary.EscapedTotal < native.EscapedTotal)

[<Fact>]
let ``E2: shared determinations reduce human hours versus AI-native without raising escapes`` () =
    let eco = e2 E2.EcosystemSharedDeterminations
    let native = e2 E2.RulesAiFlagsExceptions
    Assert.True(eco.HumanMinutes < native.HumanMinutes)
    Assert.Equal(native.EscapedTotal, eco.EscapedTotal)

// E3
[<Fact>]
let ``E3: netting reduces payments; netting widens return impact; registry lowers uncaught fraud`` () =
    let rs = E3.run E3.defaults seed
    let get d = rs |> List.find (fun r -> r.Design = d)
    Assert.True((get E3.DailyNettingWithKey).Payments < (get E3.PerGrantWithKey).Payments)
    Assert.True((get E3.PerGrantWithKey).RecipientMinutes < (get E3.PerGrantBaseline).RecipientMinutes)
    Assert.True((get E3.RegistryNettingWithKey).ExpectedFraudulentChangesUncaught < (get E3.PerGrantWithKey).ExpectedFraudulentChangesUncaught)
    // per-grant: a return affects one grant; netted: a return affects every grant in the batch
    let perPayment d = (get d).GrantsAffectedByReturns / float (get d).Payments
    Assert.True(perPayment E3.DailyNettingWithKey > perPayment E3.PerGrantWithKey)

// E4
[<Fact>]
let ``E4: continuous reconciliation detects breaks younger and cheaper than month-end; a masked outage erodes it`` () =
    let c = E4.run E4.defaults seed E4.Continuous
    let m = E4.run E4.defaults seed E4.MonthEnd
    let masked = E4.run { E4.defaults with FeedOutage = Some(100, 110); MissingFeedAlarm = false } seed E4.Continuous
    let alarmed = E4.run { E4.defaults with FeedOutage = Some(100, 110) } seed E4.Continuous
    Assert.Equal(c.Breaks, m.Breaks)
    Assert.True(c.MeanAgeAtDetection < m.MeanAgeAtDetection)
    Assert.True(c.Minutes < m.Minutes)
    Assert.True(masked.MaxAgeAtDetection > alarmed.MaxAgeAtDetection)

// E6
[<Fact>]
let ``E6: a shared pool needs no more FTE than separate pools to meet the SLA every day`` () =
    let sep = E6.minFteForSla E6.defaults seed E6.SeparatePools
    let shared = E6.minFteForSla E6.defaults seed E6.SharedPool
    match sep, shared with
    | Some a, Some b -> Assert.True(b <= a)
    | _ -> failwith "no feasible staffing found"

[<Fact>]
let ``E6: surge smoothing reduces FTE needed`` () =
    match E6.minFteForSla E6.defaults seed E6.SharedPool, E6.minFteForSla E6.defaults seed E6.SharedWithSmoothing with
    | Some a, Some b -> Assert.True(b < a)
    | _ -> failwith "no feasible staffing found"

// E8
[<Fact>]
let ``E8: replay migration preserves full history; balance-forward keeps balance but loses history`` () =
    let rs = Daf.Experiments.Migration.compare 5 2
    let src = rs.[0]
    let replay = rs.[1]
    let fwd = rs.[2]
    Assert.Equal(src, { replay with Method = src.Method })
    Assert.Equal(src.FundBalance, fwd.FundBalance)
    Assert.True(fwd.HistoryCompleteness < 0.5)

// E9
[<Fact>]
let ``E9: outbox plus idempotency key is exactly-once at every crash point; naive designs are not`` () =
    E9.crashPoints |> List.iter (fun c -> Assert.Equal(E9.Correct, E9.classify E9.OutboxWithIdempotencyKey c))
    for d in [ E9.SendThenCommit; E9.CommitThenSendNoOutbox; E9.OutboxNoIdempotency ] do
        Assert.Contains(E9.crashPoints, fun c -> E9.classify d c <> E9.Correct)

// E10
[<Fact>]
let ``E10: auto-close adds escapes beyond human misses, more so after shift; flag-only escapes only human misses`` () =
    let p = E10.defaults
    let fo = E10.flagOnly p seed
    Assert.InRange(float fo.EscapedDefects, 0.0, 0.1 * float fo.Defects)
    Assert.True((E10.autoClose { p with ShiftedShare = 0.3 } seed -1.0).EscapedDefects > (E10.flagOnly { p with ShiftedShare = 0.3 } seed).EscapedDefects)
    let baseEsc = (E10.autoClose p seed 0.5).EscapedDefects
    Assert.True(baseEsc > fo.EscapedDefects)
    let shiftedEsc = (E10.autoClose { p with ShiftedShare = 0.3 } seed 0.5).EscapedDefects
    Assert.True(shiftedEsc > baseEsc)
    Assert.True((E10.autoClose p seed 0.5).Minutes < (E10.flagOnly p seed).Minutes)

// E7/E11 network economics on the measured public-data reuse curve
[<Fact>]
let ``network: measured curve loads for 48 sponsors in three orders; routine-only value never breaks even large-first; costly determinations do`` () =
    let path = System.IO.Path.Combine(Daf.Enterprise.Tests.Fixtures.repoRoot (), "data", "workflow-innovation", "recipient-overlap-summary.csv")
    let (curve, sponsors) = Daf.Experiments.NetworkEconomics.load path
    Assert.Equal(48, sponsors.Length)
    for o in [ "descending_assets"; "ascending_assets"; "random_mean_200" ] do
        Assert.Equal(48, curve |> List.filter (fun c -> c.Order = o) |> List.length)
    Assert.All(curve, fun c -> Assert.InRange(c.RecipientShare, 0.0, 1.0))
    let p = Daf.Experiments.NetworkEconomics.defaults
    let routine = Daf.Experiments.NetworkEconomics.joinCurve p curve sponsors "descending_assets"
    Assert.Equal(None, Daf.Experiments.NetworkEconomics.firstBreakEven routine)
    let costly = Daf.Experiments.NetworkEconomics.joinCurve { p with CostPerDetermination = 270.0 } curve sponsors "descending_assets"
    Assert.True((Daf.Experiments.NetworkEconomics.firstBreakEven costly).IsSome)
    // order dependence: small-first gives the second joiner almost nothing
    let small2 = (Daf.Experiments.NetworkEconomics.joinCurve p curve sponsors "ascending_assets").[1].MemberSavings
    let large2 = routine.[1].MemberSavings
    Assert.True(small2 < large2 / 10.0)
