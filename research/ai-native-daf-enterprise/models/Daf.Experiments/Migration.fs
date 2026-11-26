/// E8 — System-of-record migration by event-log replay vs conventional balance-forward migration (W8; INN-17, INN-18).
module Daf.Experiments.Migration

open System
open Daf.Enterprise.Domain
open Daf.Enterprise.Policy
open Daf.Enterprise.Journey

let private t0 = DateTime(2023, 1, 2, 0, 0, 0, DateTimeKind.Utc)
let private donor = PartyId "P-1"
let private acct = AccountId "A-1"
let private rid = RecipientId "R-1"

let private policy =
    { Ref = { PolicyId = "p"; Version = 1 }; AutoApproveLimit = 250000m; EligibilityFreshness = TimeSpan.FromDays 35.0
      NewOrgYears = 2; DiscretionaryHolds = Set.empty; ApprovedBy = "board" }

let private recipient = { Id = rid; LegalName = "R"; Ein = Some(Ein "11-1111111"); IsFiscalSponsor = false; RelatedPartyIds = [] }

let private ctx (at: DateTime) (r: Recommendation) =
    { Now = at; Recommendation = r; Recipient = recipient; AccountParties = Set.singleton donor; AgentFlags = []
      Eligibility = Some { Recipient = rid; Ein = recipient.Ein; Class = PublicCharity170b1A; Revoked = false; OfacListed = false
                           RulingYear = Some 1990; Stamp = { Source = "IRS"; SourceVersion = "m"; RetrievedAt = at.AddDays -1.0 } } }

let private profile = { Recipient = rid; Rail = "ACH"; AccountToken = "t"; Verified = true; CoolingOffUntil = None }
let private limits = { PerRecipientDailyCap = 1000000m; DualControlAbove = 1000000m }

/// A dated command log: one contribution per quarter and one grant per month for `years` years.
let commandLog (years: int) : (DateTime * Command) list =
    let opening = [ t0, VerifyIdentity donor; t0, OpenAccount(acct, donor, "v1") ]
    let quarters =
        [ for q in 0 .. years * 4 - 1 do
            let at = t0.AddDays(float (q * 91))
            let ref' = $"CI-{q}"
            yield at, DeclareIntent(acct, ref', 30000m)
            yield at, SettleContribution(ref', 30000m, $"CUST-{q}", at) ]
    let months =
        [ for m in 0 .. years * 12 - 1 do
            let at = t0.AddDays(float (m * 30 + 5))
            let gid = GrantId $"G-{m}"
            let pid = PaymentId $"P-{m}"
            let r = { Account = acct; RequestedBy = donor; ViaAgent = None; Recipient = rid; Amount = 5000m; Purpose = "general"
                      Recognition = FullContact; IdempotencyKey = $"k-{m}"; SubmittedAt = at }
            yield at, SubmitRecommendation(gid, r)
            yield at, Evaluate(gid, policy, ctx at)
            yield at, ReleasePayment(gid, pid, profile, limits, at, None)
            yield at, SettlePayment(pid, $"T-{m}") ]
    opening @ quarters @ months |> List.sortBy fst

let private runLog log =
    match run empty (log |> List.map snd) with
    | Ok(s, evs) -> s, evs
    | Error(e, _) -> failwithf "%A" e

type MigrationResult =
    { Method: string
      GrantsVisible: int
      ContributionsVisible: int
      FundBalance: Usd
      ScheduleDGrantsAllYears: Usd
      HistoryCompleteness: float }

/// Replay migration: the target system consumes the full log and reproduces every projection.
/// Balance-forward migration (what AEF's donors experienced: two years of history, EV-037): the
/// target receives an opening balance plus the last `keepYears` years of activity.
let compare (years: int) (keepYears: int) =
    let log = commandLog years
    let (src, srcEvents) = runLog log
    let (replayed, replayEvents) = runLog log
    let cutoff = t0.AddDays(float (365 * (years - keepYears)))
    let (before, after) = log |> List.partition (fun (at, _) -> at < cutoff)
    let (atCutoff, _) = runLog before
    let openingBalance = available atCutoff acct
    let forward =
        [ t0, VerifyIdentity donor; t0, OpenAccount(acct, donor, "v1")
          cutoff, DeclareIntent(acct, "OPENING", openingBalance)
          cutoff, SettleContribution("OPENING", openingBalance, "MIGRATION-OPENING", cutoff) ]
        @ (after |> List.filter (fun (_, c) -> match c with VerifyIdentity _ | OpenAccount _ -> false | _ -> true))
    let (fwd, fwdEvents) = runLog forward
    let grants (evs: Event list) = evs |> List.filter (function PaymentSettled _ -> true | _ -> false) |> List.length
    let contribs (evs: Event list) = evs |> List.filter (function ContributionSettled(_, r, _, _) -> r <> "OPENING" | _ -> false) |> List.length
    let srcGrants = grants srcEvents
    let row name (s: State) evs =
        { Method = name; GrantsVisible = grants evs; ContributionsVisible = contribs evs; FundBalance = available s acct
          ScheduleDGrantsAllYears = (scheduleD s evs).GrantsPaid
          HistoryCompleteness = float (grants evs) / float srcGrants }
    [ row "source system" src srcEvents
      row "replay migration (event log)" replayed replayEvents
      row $"balance-forward migration ({keepYears}-year history)" fwd fwdEvents ]
