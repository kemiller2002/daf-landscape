/// Workflow-innovation experiments (workflow-innovation/08-experiments). Synthetic, seeded, pure.
/// Every parameter is an assumption [A] unless its doc comment cites repository evidence.
/// Results are experiment outputs [X] about MODELS, not measurements of any organization.
module Daf.Experiments.Experiments

open System
open Daf.Experiments.Sim

// ======================================================================================
// E1 — Recipient verification architectures (W1; INN-01, INN-02, INN-03, INN-34)
// ======================================================================================
module E1 =
    type Params =
        { Grants: int
          Recipients: int
          ZipfS: float                    // concentration; calibrated so top ranks hold most grants
          AnnualIneligibleRate: float     // recipients losing eligibility per year [A]; revoked-EIN grants are 0.082% of top-50 dollars (strategic synthesis §0)
          IrsPublicationDays: int         // IRS bulk files refreshed about monthly [A]
          HumanLookupMinutes: float       // per manual lookup [A]
          HumanMissRate: float            // manual lookup errors [A]
          NetworkSponsors: int            // sponsors sharing a passport (ecosystem design)
          NetworkOverlap: float }         // E7 measured: a shared record avoids 51.3% of sponsor-recipient checks across 48 top-50 sponsors (FY2023 Schedule I)

    let defaults =
        { Grants = 100000; Recipients = 12000; ZipfS = 1.0; AnnualIneligibleRate = 0.005
          IrsPublicationDays = 30; HumanLookupMinutes = 3.0; HumanMissRate = 0.01
          NetworkSponsors = 48; NetworkOverlap = 0.513 }

    type Arch =
        | ManualPerGrant
        | AutomatedPerGrant
        | PassportOnPublication     // naive: re-verify every known recipient at each publication
        | PassportDiffDriven        // verify each recipient once, then process only source changes (INN-34)
        | PassportQuarterly
        | NetworkPassport

    type Result =
        { Arch: Arch
          VerificationOps: float          // lookups or refresh operations performed by this sponsor
          HumanMinutes: float
          IneligibleGrants: int           // grants made on or after the recipient's change date
          Escaped: int                    // ineligible grants not caught before approval
          SourceLatencyFloor: int         // escapes that NO architecture can catch (change not yet published)
          MedianLatencySeconds: float }

    /// Day the change becomes visible in data refreshed every `period` days.
    let visibleDay period change = ((change / period) + 1) * period

    let run (p: Params) (seed: uint64) : Result list =
        let z = zipf p.Recipients p.ZipfS
        let rng0 = Rng seed
        // per-recipient eligibility change day (or none)
        let (changes, rng1) =
            draws p.Recipients (fun r ->
                let (hit, r1) = bernoulli p.AnnualIneligibleRate r
                let (u, r2) = uniform r1
                (if hit then Some(int (u * 365.0)) else None), r2) rng0
        let changeArr = Array.ofList changes
        let (grants, rng2) =
            draws p.Grants (fun r ->
                let (rec', r1) = sampleZipf z r
                let (u, r2) = uniform r1
                (rec', int (u * 365.0)), r2) rng1
        let (misses, _) = draws p.Grants (bernoulli p.HumanMissRate) rng2
        let ineligible =
            grants |> List.map (fun (rc, day) -> match changeArr.[rc] with Some c -> day >= c | None -> false)
        let caughtWith period =
            List.map2 (fun (rc, day) inel -> inel && (match changeArr.[rc] with Some c -> visibleDay period c <= day | None -> false)) grants ineligible
        let caughtIrs = caughtWith p.IrsPublicationDays
        let caughtQuarterly = caughtWith 90
        let count = List.filter id >> List.length
        let nInel = count ineligible
        let floor = List.map2 (fun i c -> i && not c) ineligible caughtIrs |> count
        let distinctRecipients = grants |> List.map fst |> List.distinct |> List.length |> float
        let refreshes period = distinctRecipients * (365.0 / float period)
        let escapedManual = List.map3 (fun i c m -> i && (not c || m)) ineligible caughtIrs misses |> count
        [ { Arch = ManualPerGrant; VerificationOps = float p.Grants; HumanMinutes = float p.Grants * p.HumanLookupMinutes
            IneligibleGrants = nInel; Escaped = escapedManual; SourceLatencyFloor = floor; MedianLatencySeconds = 24.0 * 3600.0 }
          { Arch = AutomatedPerGrant; VerificationOps = float p.Grants; HumanMinutes = 0.0
            IneligibleGrants = nInel; Escaped = nInel - count caughtIrs; SourceLatencyFloor = floor; MedianLatencySeconds = 2.0 }
          { Arch = PassportOnPublication; VerificationOps = refreshes p.IrsPublicationDays; HumanMinutes = 0.0
            IneligibleGrants = nInel; Escaped = nInel - count caughtIrs; SourceLatencyFloor = floor; MedianLatencySeconds = 0.01 }
          { Arch = PassportDiffDriven
            VerificationOps = distinctRecipients + float (changes |> List.filter Option.isSome |> List.length)
            HumanMinutes = 0.0; IneligibleGrants = nInel; Escaped = nInel - count caughtIrs; SourceLatencyFloor = floor; MedianLatencySeconds = 0.01 }
          { Arch = PassportQuarterly; VerificationOps = refreshes 90; HumanMinutes = 0.0
            IneligibleGrants = nInel; Escaped = nInel - count caughtQuarterly; SourceLatencyFloor = floor; MedianLatencySeconds = 0.01 }
          { Arch = NetworkPassport
            VerificationOps = (distinctRecipients + float (changes |> List.filter Option.isSome |> List.length)) * (1.0 - p.NetworkOverlap)
            HumanMinutes = 0.0; IneligibleGrants = nInel; Escaped = nInel - count caughtIrs; SourceLatencyFloor = floor; MedianLatencySeconds = 0.01 } ]

// ======================================================================================
// E2 — Approval architectures with seeded defects (W1/W2; INN-05, INN-06, INN-35; DD-005)
// ======================================================================================
module E2 =
    type Defect =
        | Clean
        | Revoked                 // ineligible recipient (data shows it)
        | SanctionsHit
        | UndeclaredRelatedParty  // §4967/§4958 risk not in declared relationships
        | PledgeOrTicketBenefit   // purpose text implies a benefit
        | AccountTakeover         // attacker-controlled new "charity" payee

    type Routing =
        | Routine
        | NeedsReview             // foreign, fiscal sponsor, new organization: legitimate but must be reviewed

    type Grant = { Defect: Defect; Routing: Routing; Day: int }

    type Params =
        { Grants: int
          Rates: (Defect * float) list          // per-grant defect base rates [A]
          NeedsReviewRate: float                // ~7–8.5% of grants per the core proxy (EV-081); 0.08 used
          RuleCatch: Defect -> float            // deterministic rule detection probability [A]
          AiRecall: Defect -> float             // AI flagger recall per defect type [A]
          AiFalsePositive: float                // AI flags on clean routine grants [A]
          HumanRoutineCatch: Defect -> float    // reviewer looking at a routine grant without a dossier [A]
          HumanExceptionCatch: float            // reviewer with dossier on a flagged case [A]
          MinutesRoutineReview: float           // per-grant manual review [A]
          MinutesException: float               // per exception with dossier (parent model: 45) [A]
          SampleRate: float                     // acceptance sampling of auto-approved grants [A]
          ReuseShareOfReviews: float            // share of NeedsReview resolved by reusable determination (INN-04) [A]
          MinutesReusedReview: float
          AutoClearShare: float                 // unsafe variant: share of flags an AI auto-clears [A]
          MisconfigWindow: (int * int) option } // revocation rule silently disabled [start, end) — adversarial

    let defaults =
        { Grants = 200000
          Rates = [ Revoked, 0.001; SanctionsHit, 0.00005; UndeclaredRelatedParty, 0.002; PledgeOrTicketBenefit, 0.003; AccountTakeover, 0.0005 ]
          NeedsReviewRate = 0.08
          RuleCatch = (function Revoked -> 1.0 | SanctionsHit -> 1.0 | AccountTakeover -> 0.6 | UndeclaredRelatedParty -> 0.0 | PledgeOrTicketBenefit -> 0.0 | Clean -> 0.0)
          AiRecall = (function UndeclaredRelatedParty -> 0.6 | PledgeOrTicketBenefit -> 0.7 | AccountTakeover -> 0.5 | Revoked -> 0.0 | SanctionsHit -> 0.0 | Clean -> 0.0)
          AiFalsePositive = 0.02
          HumanRoutineCatch = (function Revoked -> 0.95 | SanctionsHit -> 0.9 | UndeclaredRelatedParty -> 0.3 | PledgeOrTicketBenefit -> 0.5 | AccountTakeover -> 0.2 | Clean -> 0.0)
          HumanExceptionCatch = 0.95
          MinutesRoutineReview = 6.0
          MinutesException = 45.0
          SampleRate = 0.02
          ReuseShareOfReviews = 0.5
          MinutesReusedReview = 5.0
          AutoClearShare = 0.5
          MisconfigWindow = None }

    type Arch =
        | ManualReviewAll          // conventional baseline
        | RulesPlusManualAll       // automation-first
        | RulesAiFlagsExceptions   // AI-native (flag-only)
        | RulesAiFlagsWithCanaries // AI-native + daily known-answer canary grants through the live rules (CTL-046)
        | RulesSamplingNoAi        // radical: no per-item review, acceptance sampling
        | EcosystemSharedDeterminations // AI-native + reusable determinations
        | AiAutoClearUnsafe        // violates DD-005; included as adversarial comparator
        | PayFirstPreverified      // INN-35 radical: pay routine first, sample after

    type Result =
        { Arch: Arch
          HumanMinutes: float
          HumanCases: int
          Escaped: Map<Defect, int>
          EscapedTotal: int
          DefectsTotal: int
          MisconfigDetectedDay: int option   // first day a systemic rule failure is noticed
          RoutineLatency: string }

    let generate (p: Params) seed =
        let pick (u: float) =
            p.Rates |> List.fold (fun (acc, chosen) (d, r) ->
                match chosen with
                | Some _ -> (acc, chosen)
                | None -> if u < acc + r then (acc + r, Some d) else (acc + r, None)) (0.0, None)
            |> snd |> Option.defaultValue Clean
        draws p.Grants (fun r ->
            let (u, r1) = uniform r
            let (nr, r2) = bernoulli p.NeedsReviewRate r1
            let (d, r3) = uniform r2
            { Defect = pick u; Routing = (if nr then NeedsReview else Routine); Day = int (d * 365.0) }, r3) (Rng seed)
        |> fst

    let private inWindow day = function Some(a, b) -> day >= a && day < b | None -> false

    let run (p0: Params) (seed: uint64) (arch: Arch) : Result =
        let grants = generate p0 seed
        // canaries detect a broken rule on its first day; the rule is restored the next day (fix lag 1 day [A])
        let p =
            match arch, p0.MisconfigWindow with
            | RulesAiFlagsWithCanaries, Some(a, _) -> { p0 with MisconfigWindow = Some(a, a + 1) }
            | _ -> p0
        let rec walk (gs: Grant list) (rng: Rng) (minutes, cases, escaped: Map<Defect, int>, firstDetect: int option) =
            match gs with
            | [] -> (minutes, cases, escaped, firstDetect)
            | g :: rest ->
                let (u1, r1) = uniform rng
                let (u2, r2) = uniform r1
                let (u3, r3) = uniform r2
                let (u4, r4) = uniform r3
                let ruleCatch =
                    let base' = p.RuleCatch g.Defect
                    let disabled = g.Defect = Revoked && inWindow g.Day p.MisconfigWindow
                    u1 < (if disabled then 0.0 else base')
                let aiFlag = (g.Defect = Clean && u2 < p.AiFalsePositive) || (g.Defect <> Clean && u2 < p.AiRecall g.Defect)
                let needsHuman = g.Routing = NeedsReview
                let isDefect = g.Defect <> Clean
                // returns (minutes, case?, caught?, systemic-detection?)
                let (m, c, caught, sysDetect) =
                    match arch with
                    | ManualReviewAll ->
                        let catchP = if needsHuman then max (p.HumanRoutineCatch g.Defect) 0.0 else p.HumanRoutineCatch g.Defect
                        p.MinutesRoutineReview + (if needsHuman then p.MinutesException else 0.0), true, (isDefect && u3 < catchP), (isDefect && g.Defect = Revoked && u3 < catchP)
                    | RulesPlusManualAll ->
                        let caught = isDefect && (ruleCatch || u3 < p.HumanRoutineCatch g.Defect)
                        p.MinutesRoutineReview + (if needsHuman then p.MinutesException else 0.0), true, caught, (isDefect && g.Defect = Revoked && not ruleCatch && caught)
                    | RulesAiFlagsExceptions | RulesAiFlagsWithCanaries | EcosystemSharedDeterminations | AiAutoClearUnsafe | PayFirstPreverified ->
                        let flagged = ruleCatch || aiFlag
                        let toHuman =
                            match arch with
                            | AiAutoClearUnsafe -> (flagged && not (aiFlag && not ruleCatch && u4 < p.AutoClearShare)) || needsHuman
                            | _ -> flagged || needsHuman
                        let reviewMinutes =
                            match arch with
                            | EcosystemSharedDeterminations when needsHuman && not flagged && u4 < p.ReuseShareOfReviews -> p.MinutesReusedReview
                            | _ -> p.MinutesException
                        let caughtPre = isDefect && toHuman && (flagged || needsHuman) && u3 < p.HumanExceptionCatch
                        // pay-first: routine grants are paid before rules run; only sampling sees them afterwards
                        let caught =
                            match arch with
                            | PayFirstPreverified when not needsHuman -> false
                            | _ -> caughtPre && (flagged || (needsHuman && (p.HumanRoutineCatch g.Defect > u3)))
                        let sampled = (arch = PayFirstPreverified) && not needsHuman && u4 < p.SampleRate && isDefect
                        (if toHuman then reviewMinutes else 0.0) + (if sampled then p.MinutesRoutineReview else 0.0), toHuman, caught, sampled && g.Defect = Revoked
                    | RulesSamplingNoAi ->
                        let toHuman = ruleCatch || needsHuman
                        let caught = isDefect && toHuman && u3 < (if ruleCatch then p.HumanExceptionCatch else p.HumanRoutineCatch g.Defect)
                        let sampled = (not toHuman) && u4 < p.SampleRate
                        let sysDetect = sampled && g.Defect = Revoked && u3 < 0.95
                        (if toHuman then p.MinutesException else 0.0) + (if sampled then p.MinutesRoutineReview else 0.0), toHuman, caught, sysDetect
                let escaped' = if isDefect && not caught then escaped.Add(g.Defect, (escaped.TryFind g.Defect |> Option.defaultValue 0) + 1) else escaped
                let firstDetect' =
                    match firstDetect with
                    | None when sysDetect && inWindow g.Day p.MisconfigWindow -> Some g.Day
                    | f -> f
                walk rest r4 (minutes + m, cases + (if c then 1 else 0), escaped', firstDetect')
        let sorted = grants |> List.sortBy (fun g -> g.Day)
        let (minutes0, cases, escaped, firstDetect0) = walk sorted (Rng(seed + 7UL)) (0.0, 0, Map.empty, None)
        // canaries: one known-revoked synthetic grant per day; a failure is seen the day the rule breaks
        let canaryDetect = match arch, p0.MisconfigWindow with RulesAiFlagsWithCanaries, Some(a, _) -> Some a | _ -> None
        let firstDetect = match canaryDetect with Some d -> Some d | None -> firstDetect0
        let minutes = minutes0 + (match arch with RulesAiFlagsWithCanaries -> 365.0 * 1.0 | _ -> 0.0)
        { Arch = arch
          HumanMinutes = minutes
          HumanCases = cases
          Escaped = escaped
          EscapedTotal = escaped |> Map.toList |> List.sumBy snd
          DefectsTotal = grants |> List.filter (fun g -> g.Defect <> Clean) |> List.length
          MisconfigDetectedDay = firstDetect
          RoutineLatency =
            match arch with
            | ManualReviewAll | RulesPlusManualAll -> "queue (days)"
            | PayFirstPreverified -> "seconds (paid before checks)"
            | _ -> "seconds (rule decision)" }

    let archs = [ ManualReviewAll; RulesPlusManualAll; RulesAiFlagsExceptions; RulesAiFlagsWithCanaries; RulesSamplingNoAi; EcosystemSharedDeterminations; AiAutoClearUnsafe; PayFirstPreverified ]

// ======================================================================================
// E3 — Disbursement: per-grant vs daily netting; remittance key; payee registry (W3; INN-07/08/09)
// ======================================================================================
module E3 =
    type Params =
        { Grants: int
          Recipients: int
          ZipfS: float
          CheckShareBaseline: float      // Fidelity reports 67% of grants by EFT (industry report §2.5) => 33% non-EFT
          CheckShareRegistry: float      // design target with recipient registry [A]
          AchCost: float                 // [A]
          CheckCost: float               // [A]
          RecipientMinutesNoKey: float   // matching a grant without a grant ID in remittance [A]
          RecipientMinutesWithKey: float // [A]
          PayeeChangesPerRecipientYear: float // [A]
          FraudShareOfChanges: float     // [A]
          CallbackCatchPerSponsor: float // per-sponsor callback verification [A]
          RegistryCatch: float           // registry out-of-band + cooling-off [A]
          SponsorsPerRecipient: float    // recipients deal with several sponsors [A]; E7 measures overlap
          ReturnRate: float }            // payment returns [A]

    let defaults =
        { Grants = 100000; Recipients = 12000; ZipfS = 1.0; CheckShareBaseline = 0.33; CheckShareRegistry = 0.10
          AchCost = 0.30; CheckCost = 4.0; RecipientMinutesNoKey = 5.0; RecipientMinutesWithKey = 0.5
          PayeeChangesPerRecipientYear = 0.2; FraudShareOfChanges = 0.02; CallbackCatchPerSponsor = 0.7
          RegistryCatch = 0.95; SponsorsPerRecipient = 3.0; ReturnRate = 0.005 }

    type Design =
        | PerGrantBaseline       // one payment per grant, 33% checks, no grant ID
        | PerGrantWithKey        // automation-first: structured remittance
        | DailyNettingWithKey    // radical: one payment per recipient per day
        | RegistryNettingWithKey // ecosystem: shared payee registry + netting + key

    type Result =
        { Design: Design
          Payments: int
          PaymentCost: float
          RecipientMinutes: float
          ExpectedFraudulentChangesUncaught: float
          GrantsAffectedByReturns: float }

    let run (p: Params) (seed: uint64) : Result list =
        let z = zipf p.Recipients p.ZipfS
        let (grants, _) =
            draws p.Grants (fun r ->
                let (rc, r1) = sampleZipf z r
                let (u, r2) = uniform r1
                (rc, int (u * 250.0)), r2) (Rng seed)   // 250 business days
        let nettedPayments = grants |> List.distinct |> List.length
        let grantsPerNetted = float p.Grants / float nettedPayments
        let fraudAttempts = float p.Recipients * p.PayeeChangesPerRecipientYear * p.FraudShareOfChanges
        let cost payments checkShare = float payments * (checkShare * p.CheckCost + (1.0 - checkShare) * p.AchCost)
        let returns payments perPayment = float payments * p.ReturnRate * perPayment
        [ { Design = PerGrantBaseline; Payments = p.Grants; PaymentCost = cost p.Grants p.CheckShareBaseline
            RecipientMinutes = float p.Grants * p.RecipientMinutesNoKey
            ExpectedFraudulentChangesUncaught = fraudAttempts * p.SponsorsPerRecipient * (1.0 - p.CallbackCatchPerSponsor) / p.SponsorsPerRecipient
            GrantsAffectedByReturns = returns p.Grants 1.0 }
          { Design = PerGrantWithKey; Payments = p.Grants; PaymentCost = cost p.Grants p.CheckShareBaseline
            RecipientMinutes = float p.Grants * p.RecipientMinutesWithKey
            ExpectedFraudulentChangesUncaught = fraudAttempts * (1.0 - p.CallbackCatchPerSponsor)
            GrantsAffectedByReturns = returns p.Grants 1.0 }
          { Design = DailyNettingWithKey; Payments = nettedPayments; PaymentCost = cost nettedPayments p.CheckShareBaseline
            RecipientMinutes = float p.Grants * p.RecipientMinutesWithKey
            ExpectedFraudulentChangesUncaught = fraudAttempts * (1.0 - p.CallbackCatchPerSponsor)
            GrantsAffectedByReturns = returns nettedPayments grantsPerNetted }
          { Design = RegistryNettingWithKey; Payments = nettedPayments; PaymentCost = cost nettedPayments p.CheckShareRegistry
            RecipientMinutes = float p.Grants * p.RecipientMinutesWithKey
            ExpectedFraudulentChangesUncaught = fraudAttempts * (1.0 - p.RegistryCatch)
            GrantsAffectedByReturns = returns nettedPayments grantsPerNetted } ]

// ======================================================================================
// E4 — Reconciliation: continuous vs month-end (W11; INN-22)
// ======================================================================================
module E4 =
    type Params =
        { BreaksPerDay: float            // [A]
          BaseMinutes: float             // investigation minutes for a fresh break [A]
          MinutesPerAgeDay: float        // evidence decays with age [A] (stated assumption, not sourced)
          FeedOutage: (int * int) option // custodian feed missing [start, end)
          MissingFeedAlarm: bool }

    let defaults = { BreaksPerDay = 4.0; BaseMinutes = 15.0; MinutesPerAgeDay = 2.0; FeedOutage = None; MissingFeedAlarm = true }

    type Mode = Continuous | MonthEnd

    type Result = { Mode: Mode; Breaks: int; MeanAgeAtDetection: float; MaxAgeAtDetection: int; Minutes: float; Label: string }

    let run (p: Params) (seed: uint64) (mode: Mode) : Result =
        let (counts, _) =
            draws 365 (fun r ->
                let (u, r1) = uniform r
                // approximately Poisson via rounding of a uniform-scaled mean (simple, deterministic)
                int (Math.Round(p.BreaksPerDay * 2.0 * u)), r1) (Rng seed)
        let detectDay day =
            let outageDelay =
                match p.FeedOutage with
                | Some(a, b) when day >= a && day < b -> if p.MissingFeedAlarm then 1 else b - day
                | _ -> 0
            match mode with
            | Continuous -> day + outageDelay
            | MonthEnd -> max ((day / 30 + 1) * 30) (day + outageDelay)
        let ages = counts |> List.mapi (fun day n -> List.replicate n (detectDay day - day)) |> List.concat
        let minutes = ages |> List.sumBy (fun a -> p.BaseMinutes + p.MinutesPerAgeDay * float a)
        { Mode = mode; Breaks = ages.Length
          MeanAgeAtDetection = (if ages.IsEmpty then 0.0 else ages |> List.averageBy float)
          MaxAgeAtDetection = (if ages.IsEmpty then 0 else List.max ages)
          Minutes = minutes
          Label = (match p.FeedOutage with Some _ -> (if p.MissingFeedAlarm then "outage with missing-feed alarm" else "outage without alarm (masked)") | None -> "no outage") }

// ======================================================================================
// E5 — Onboarding designs (W12; INN-24, INN-25). Assumption-dominated; see results caveat.
// ======================================================================================
module E5 =
    type Design =
        { Name: string
          StepsBeforeFirstGift: int
          AbandonPerStep: float      // [A]
          DonorMinutes: float        // [A]
          FraudDetectBeforeFirstGrant: float  // synthetic-identity detection before money moves [A]
          DataCompleteAtGrant: float }        // share of later-needed fields present when first needed [A]

    let designs =
        [ { Name = "conventional upfront application (PDF/web form, wet or e-sign)"; StepsBeforeFirstGift = 9; AbandonPerStep = 0.04; DonorMinutes = 35.0; FraudDetectBeforeFirstGrant = 0.90; DataCompleteAtGrant = 0.95 }
          { Name = "automation-first form with prefill"; StepsBeforeFirstGift = 6; AbandonPerStep = 0.03; DonorMinutes = 15.0; FraudDetectBeforeFirstGrant = 0.90; DataCompleteAtGrant = 0.95 }
          { Name = "AI-native conversational progressive intake"; StepsBeforeFirstGift = 4; AbandonPerStep = 0.025; DonorMinutes = 8.0; FraudDetectBeforeFirstGrant = 0.88; DataCompleteAtGrant = 0.90 }
          { Name = "radical: account at first contribution intent + step-up before first grant"; StepsBeforeFirstGift = 2; AbandonPerStep = 0.02; DonorMinutes = 3.0; FraudDetectBeforeFirstGrant = 0.90; DataCompleteAtGrant = 0.85 }
          { Name = "ecosystem: upstream custodian/advisor KYC attestation reuse"; StepsBeforeFirstGift = 2; AbandonPerStep = 0.02; DonorMinutes = 2.0; FraudDetectBeforeFirstGrant = 0.85; DataCompleteAtGrant = 0.92 } ]

    type Result = { Name: string; CompletionRate: float; DonorMinutes: float; FraudulentAccountsReachingGrantPer10k: float; DataCompleteAtGrant: float }

    /// Synthetic-identity attempt rate 0.2% of applicants [A].
    let evaluate (fraudRate: float) (d: Design) =
        let completion = Math.Pow(1.0 - d.AbandonPerStep, float d.StepsBeforeFirstGift)
        { Name = d.Name; CompletionRate = completion; DonorMinutes = d.DonorMinutes
          FraudulentAccountsReachingGrantPer10k = 10000.0 * fraudRate * (1.0 - d.FraudDetectBeforeFirstGrant)
          DataCompleteAtGrant = d.DataCompleteAtGrant }

// ======================================================================================
// E6 — Specialist pooling across sponsors and surge smoothing (W2/W4; INN-28, INN-37)
// ======================================================================================
module E6 =
    type Params =
        { Sponsors: int
          MeanCasesPerDayPerSponsor: float  // [A]
          SurgeMultiplier: float            // December [A]
          CasesPerFtePerDay: float          // [A] e.g. 6.4 h / 0.75 h ≈ 8.5
          Headroom: float                   // staffing above mean [A]
          SlaDays: float }

    let defaults = { Sponsors = 5; MeanCasesPerDayPerSponsor = 20.0; SurgeMultiplier = 3.0; CasesPerFtePerDay = 8.5; Headroom = 0.25; SlaDays = 2.0 }

    type Design = SeparatePools | SharedPool | SeparateWithSmoothing | SharedWithSmoothing

    type Result = { Design: Design; Fte: float; DaysOverSla: int; MaxBacklogDays: float }

    let private demand (p: Params) smoothing seed =
        // per-sponsor daily demand with noise; December (day 335–364) surge; smoothing moves half of the
        // December excess into November (day 305–334) via execution windows
        draws p.Sponsors (fun r ->
            draws 365 (fun r2 ->
                let (u, r3) = uniform r2
                (0.7 + 0.6 * u), r3) r
            |> fun (noise, r') ->
                let series =
                    noise |> List.mapi (fun day k ->
                        let surge = if day >= 335 then p.SurgeMultiplier else 1.0
                        let base' = p.MeanCasesPerDayPerSponsor * k
                        if not smoothing then base' * surge
                        elif day >= 335 then base' * (1.0 + (p.SurgeMultiplier - 1.0) / 2.0)
                        elif day >= 305 then base' * (1.0 + (p.SurgeMultiplier - 1.0) / 2.0)
                        else base')
                series, r') (Rng seed)
        |> fst

    let private simulateQueue (capacityPerDay: float) (arrivals: float list) (sla: float) =
        arrivals
        |> List.fold (fun (backlog, over, maxDays) a ->
            let avail = backlog + a
            let served = min avail capacityPerDay
            let b = avail - served
            let waitDays = if capacityPerDay > 0.0 then b / capacityPerDay else 999.0
            (b, over + (if waitDays > sla then 1 else 0), max maxDays waitDays)) (0.0, 0, 0.0)
        |> fun (_, over, maxDays) -> over, maxDays

    let run (p: Params) (seed: uint64) (design: Design) : Result =
        let smoothing = match design with SeparateWithSmoothing | SharedWithSmoothing -> true | _ -> false
        let series = demand p smoothing seed
        let ftePerSponsor = Math.Ceiling(p.MeanCasesPerDayPerSponsor * (1.0 + p.Headroom) / p.CasesPerFtePerDay)
        let totalFte = ftePerSponsor * float p.Sponsors
        match design with
        | SeparatePools | SeparateWithSmoothing ->
            let results = series |> List.map (fun s -> simulateQueue (ftePerSponsor * p.CasesPerFtePerDay) s p.SlaDays)
            { Design = design; Fte = totalFte; DaysOverSla = results |> List.sumBy fst; MaxBacklogDays = results |> List.map snd |> List.max }
        | SharedPool | SharedWithSmoothing ->
            let pooled = series |> List.transpose |> List.map List.sum
            let (over, maxDays) = simulateQueue (totalFte * p.CasesPerFtePerDay) pooled p.SlaDays
            // days over SLA reported per sponsor-day for comparability (pooled day counts once per sponsor)
            { Design = design; Fte = totalFte; DaysOverSla = over * p.Sponsors; MaxBacklogDays = maxDays }

    /// Smallest total FTE that meets the SLA on every day.
    let minFteForSla (p: Params) (seed: uint64) (design: Design) =
        [ 1.0 .. 1.0 .. 400.0 ]
        |> List.tryFind (fun fte ->
            let p' = { p with Headroom = (fte / float p.Sponsors * p.CasesPerFtePerDay / p.MeanCasesPerDayPerSponsor) - 1.0 }
            let series = demand p' (match design with SeparateWithSmoothing | SharedWithSmoothing -> true | _ -> false) seed
            match design with
            | SeparatePools | SeparateWithSmoothing ->
                let per = Math.Floor(fte / float p.Sponsors)
                per > 0.0 && (series |> List.forall (fun s -> fst (simulateQueue (per * p.CasesPerFtePerDay) s p.SlaDays) = 0))
            | SharedPool | SharedWithSmoothing ->
                fst (simulateQueue (fte * p.CasesPerFtePerDay) (series |> List.transpose |> List.map List.sum) p.SlaDays) = 0)

// ======================================================================================
// E9 — Failure recovery after interrupted payment transactions (INN-18; event catalog §2)
// ======================================================================================
module E9 =
    type CrashPoint =
        | NoCrash
        | BeforeCommit              // process dies before the approval transaction commits
        | AfterCommitBeforeSend     // committed, instruction not yet sent
        | AfterSendBeforeBank       // sent, lost in transit
        | AfterBankBeforeAck        // bank executed, acknowledgment lost
        | DuplicateDelivery         // message delivered twice

    type Design =
        | SendThenCommit            // naive: call the bank, then record
        | CommitThenSendNoOutbox    // naive: record, then call the bank in the same process (no durable intent)
        | OutboxNoIdempotency       // durable outbox, bank does not deduplicate
        | OutboxWithIdempotencyKey  // the design (DD-006 + payment gate key)

    /// Number of times the bank executes the payment for one approved grant, after recovery
    /// (restart retries any durable-but-unacknowledged intent). Correct answer: exactly 1
    /// if the approval committed, 0 if it did not.
    let executions (design: Design) (crash: CrashPoint) : int * bool =
        // returns (bank executions, approval committed)
        match design, crash with
        | _, NoCrash -> 1, true
        | _, BeforeCommit -> (match design with SendThenCommit -> 1, false | _ -> 0, false)
        | SendThenCommit, AfterCommitBeforeSend -> 1, true
        | SendThenCommit, AfterSendBeforeBank -> 0, false        // nothing recorded, payment lost: no retry
        | SendThenCommit, AfterBankBeforeAck -> 1, false         // paid but not recorded
        | SendThenCommit, DuplicateDelivery -> 2, true
        | CommitThenSendNoOutbox, AfterCommitBeforeSend -> 0, true   // no durable intent: never sent
        | CommitThenSendNoOutbox, AfterSendBeforeBank -> 0, true
        | CommitThenSendNoOutbox, AfterBankBeforeAck -> 1, true
        | CommitThenSendNoOutbox, DuplicateDelivery -> 2, true
        | OutboxNoIdempotency, AfterCommitBeforeSend -> 1, true      // relay sends on restart
        | OutboxNoIdempotency, AfterSendBeforeBank -> 1, true        // relay resends
        | OutboxNoIdempotency, AfterBankBeforeAck -> 2, true         // relay resends; bank pays again
        | OutboxNoIdempotency, DuplicateDelivery -> 2, true
        | OutboxWithIdempotencyKey, AfterCommitBeforeSend -> 1, true
        | OutboxWithIdempotencyKey, AfterSendBeforeBank -> 1, true
        | OutboxWithIdempotencyKey, AfterBankBeforeAck -> 1, true    // bank deduplicates on key
        | OutboxWithIdempotencyKey, DuplicateDelivery -> 1, true

    let crashPoints = [ NoCrash; BeforeCommit; AfterCommitBeforeSend; AfterSendBeforeBank; AfterBankBeforeAck; DuplicateDelivery ]
    let designs = [ SendThenCommit; CommitThenSendNoOutbox; OutboxNoIdempotency; OutboxWithIdempotencyKey ]

    type Outcome = Correct | DoublePayment | LostPayment | PaidButUnrecorded

    let classify design crash =
        match executions design crash with
        | 1, true -> Correct
        | 0, false -> Correct              // nothing approved, nothing paid
        | n, true when n >= 2 -> DoublePayment
        | 0, true -> LostPayment
        | _, false -> PaidButUnrecorded
        | _ -> DoublePayment

// ======================================================================================
// E10 — AI exception triage: flag-only vs auto-close, with distribution shift (DD-005)
// ======================================================================================
module E10 =
    type Params =
        { Exceptions: int
          TrueDefectShare: float      // share of exceptions that are real problems [A]
          SignalStrength: float       // separation of defect vs clean scores (in noise units) [A]
          ShiftedSignal: float        // a new pattern the model was not trained on [A]
          ShiftedShare: float         // share of defects that are the new pattern [A]
          MinutesHuman: float         // [A]
          MinutesHumanWithDossier: float } // [A]

    let defaults = { Exceptions = 20000; TrueDefectShare = 0.05; SignalStrength = 2.0; ShiftedSignal = 0.3; ShiftedShare = 0.0; MinutesHuman = 45.0; MinutesHumanWithDossier = 30.0 }

    type Result = { Policy: string; Threshold: float; Minutes: float; EscapedDefects: int; Defects: int; AutoClosed: int }

    let private scores (p: Params) seed =
        draws p.Exceptions (fun r ->
            let (isDef, r1) = bernoulli p.TrueDefectShare r
            let (shifted, r2) = bernoulli p.ShiftedShare r1
            // approximate normal noise via sum of 4 uniforms (Irwin–Hall), scaled
            let (u1, r3) = uniform r2
            let (u2, r4) = uniform r3
            let (u3, r5) = uniform r4
            let (u4, r6) = uniform r5
            let noise = (u1 + u2 + u3 + u4 - 2.0) * Math.Sqrt 3.0
            let signal = if isDef then (if shifted then p.ShiftedSignal else p.SignalStrength) else 0.0
            (isDef, signal + noise), r6) (Rng seed)
        |> fst

    /// Flag-only: every exception goes to a human; AI only prepares a dossier (minutes fall).
    let flagOnly (p: Params) seed =
        let s = scores p seed
        { Policy = "flag-only (human decides every exception; AI dossier)"; Threshold = nan
          Minutes = float s.Length * p.MinutesHumanWithDossier; EscapedDefects = 0
          Defects = s |> List.filter fst |> List.length; AutoClosed = 0 }

    /// Auto-close: exceptions scoring below threshold are closed without human review.
    let autoClose (p: Params) seed (threshold: float) =
        let s = scores p seed
        let closed = s |> List.filter (fun (_, sc) -> sc < threshold)
        { Policy = "auto-close below threshold"; Threshold = threshold
          Minutes = float (s.Length - closed.Length) * p.MinutesHumanWithDossier
          EscapedDefects = closed |> List.filter fst |> List.length
          Defects = s |> List.filter fst |> List.length
          AutoClosed = closed.Length }
