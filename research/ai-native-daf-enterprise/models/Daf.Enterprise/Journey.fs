/// End-to-end reference journey (addendum §24) as a pure state machine:
///   handle : State -> Command -> Result<State * Event list, Rejection>
/// Onboarding -> contribution -> custody/accounting -> recommendation -> eligibility ->
/// authorization -> disbursement -> settlement -> reconciliation -> reporting.
module Daf.Enterprise.Journey

open System
open Daf.Enterprise.Domain
open Daf.Enterprise.Policy
open Daf.Enterprise.Ledger

// ---------- events (names match 06-data-and-knowledge/events.csv) ----------
type Event =
    | AccountOpened of AccountId * PartyId * agreementVersion: string
    | ContributionIntentDeclared of AccountId * reference: string * Usd
    | ContributionSettled of AccountId * reference: string * Usd * custodianRef: string
    | AcknowledgmentIssued of AccountId * reference: string * text: string
    | RecommendationSubmitted of GrantId * Recommendation
    | GrantFlagged of GrantId * Flag
    | GrantApproved of GrantId * Actor
    | GrantDeclined of GrantId * string
    | ExceptionCaseOpened of GrantId * Flag list
    | ExceptionCaseResolved of GrantId * Actor
    | PaymentInstructed of PaymentInstruction
    | PaymentSettled of PaymentId * settlementRef: string
    | PaymentReturned of PaymentId * returnCode: string
    | ReconciliationBreakDetected of string
    | EvidenceRecorded of EvidenceRecord

type Rejection =
    | UnknownAccount of AccountId
    | IdentityNotVerified of PartyId
    | NotPrivileged of PartyId * AccountId
    | UnknownIntent of string
    | UnknownGrant of GrantId
    | DuplicateIdempotencyKey of string
    | InvalidState of GrantId * GrantState * attempted: string
    | AgentCannotAuthorize of string
    | PaymentGateFailed of string list
    | HumanDecisionFailed of HumanDecisionError
    | UnknownPayment of PaymentId

type Account =
    { Id: AccountId
      Donor: PartyId
      Privileged: Set<PartyId> }

type State =
    { Accounts: Map<AccountId, Account>
      Verified: Set<PartyId>
      Intents: Map<string, AccountId * Usd>
      Grants: Map<GrantId, Grant>
      Payments: Map<PaymentId, PaymentInstruction * GrantId * AccountId>
      SeenKeys: Set<string>
      Journal: JournalEntry list
      Evidence: EvidenceRecord list
      PaidToday: Map<RecipientId, Usd> }

let empty =
    { Accounts = Map.empty; Verified = Set.empty; Intents = Map.empty; Grants = Map.empty
      Payments = Map.empty; SeenKeys = Set.empty; Journal = []; Evidence = []; PaidToday = Map.empty }

type PaymentLimits =
    { PerRecipientDailyCap: Usd
      DualControlAbove: Usd }

type Command =
    | VerifyIdentity of PartyId                                    // from identity provider result
    | OpenAccount of AccountId * PartyId * agreementVersion: string
    | DeclareIntent of AccountId * reference: string * Usd
    | SettleContribution of reference: string * Usd * custodianRef: string * at: DateTime
    | SubmitRecommendation of GrantId * Recommendation
    | ApplyAgentOutput of GrantId * AgentOutput * agentId: string
    | Evaluate of GrantId * GrantPolicy * (Recommendation -> DecisionContext)
    | HumanDecide of GrantId * Approver
    | AttemptApproveAs of GrantId * Actor                            // used to prove agents cannot approve
    | ReleasePayment of GrantId * PaymentId * PaymentProfile * PaymentLimits * now: DateTime * secondApprover: string option
    | SettlePayment of PaymentId * settlementRef: string
    | ReturnPayment of PaymentId * returnCode: string

let private nextEntry (s: State) = List.length s.Journal + 1
let private post (s: State) (e: JournalEntry) = { s with Journal = s.Journal @ [ e ] }

/// The acknowledgment text includes the §170(f)(18) exclusive-legal-control statement.
let acknowledgmentText (reference: string) (amount: Usd) (at: DateTime) =
    let day = at.ToString "yyyy-MM-dd"
    $"Contribution {reference}: ${amount:N2} received {day}. "
    + "The sponsoring organization has exclusive legal control over the contributed assets. "
    + "No goods or services were provided in exchange for this contribution."

/// Spendable fund balance = fund balance (approved grants already moved to payable).
let available (s: State) (a: AccountId) = balance s.Journal (FundBalance a)

let private evidence actor control subject detail at policy =
    EvidenceRecorded
        { Subject = subject; Control = control; Actor = actor; Policy = policy
          Sources = []; At = at; Detail = detail }

let private approveGrant (s: State) (gid: GrantId) (g: Grant) (actor: Actor) =
    let a = g.Recommendation.Account
    let amt = g.Recommendation.Amount
    if available s a < amt then
        Ok({ s with Grants = s.Grants.Add(gid, { g with State = Declined "insufficient fund balance" }) },
           [ GrantDeclined(gid, "insufficient fund balance") ])
    else
        let s' = post s (grantApproved (nextEntry s) a amt)
        Ok({ s' with Grants = s'.Grants.Add(gid, { g with State = Approved actor }) }, [ GrantApproved(gid, actor) ])

let handle (s: State) (cmd: Command) : Result<State * Event list, Rejection> =
    match cmd with
    | VerifyIdentity p -> Ok({ s with Verified = s.Verified.Add p }, [])

    | OpenAccount(aid, donor, ver) ->
        if not (s.Verified.Contains donor) then Error(IdentityNotVerified donor)
        else
            let acct = { Id = aid; Donor = donor; Privileged = Set.singleton donor }
            Ok({ s with Accounts = s.Accounts.Add(aid, acct) }, [ AccountOpened(aid, donor, ver) ])

    | DeclareIntent(aid, reference, amt) ->
        if not (s.Accounts.ContainsKey aid) then Error(UnknownAccount aid)
        else Ok({ s with Intents = s.Intents.Add(reference, (aid, amt)) }, [ ContributionIntentDeclared(aid, reference, amt) ])

    | SettleContribution(reference, amt, custodianRef, at) ->
        match s.Intents.TryFind reference with
        | None ->
            // Unattributable receipt: book to suspense and raise a break; never guess.
            let e = { EntryId = nextEntry s; SourceEvent = "ContributionReceived"; Postings = [ dr CashAtCustodian amt; cr Suspense amt ] }
            Ok(post s e, [ ReconciliationBreakDetected $"orphan receipt {custodianRef} ${amt}" ])
        | Some(aid, _) when s.SeenKeys.Contains custodianRef -> Error(DuplicateIdempotencyKey custodianRef)
        | Some(aid, _) ->
            let s' = post { s with SeenKeys = s.SeenKeys.Add custodianRef; Intents = s.Intents.Remove reference } (contributionSettled (nextEntry s) aid amt)
            let ack = acknowledgmentText reference amt at
            Ok(s', [ ContributionSettled(aid, reference, amt, custodianRef)
                     AcknowledgmentIssued(aid, reference, ack)
                     evidence (ExternalActor "custodian") "CTL-contribution-three-way-match" reference custodianRef at None ])

    | SubmitRecommendation(gid, r) ->
        match s.Accounts.TryFind r.Account with
        | None -> Error(UnknownAccount r.Account)
        | Some a when not (a.Privileged.Contains r.RequestedBy) -> Error(NotPrivileged(r.RequestedBy, r.Account))
        | Some _ when s.SeenKeys.Contains r.IdempotencyKey -> Error(DuplicateIdempotencyKey r.IdempotencyKey)
        | Some _ ->
            let g = { Id = gid; Recommendation = r; State = Submitted; Flags = []; Decisions = [] }
            Ok({ s with Grants = s.Grants.Add(gid, g); SeenKeys = s.SeenKeys.Add r.IdempotencyKey },
               [ RecommendationSubmitted(gid, r) ])

    | ApplyAgentOutput(gid, output, agentId) ->
        match s.Grants.TryFind gid with
        | None -> Error(UnknownGrant gid)
        | Some g ->
            match output with
            | RaiseFlag f ->
                // Whatever the agent claims, the flag is recorded as raised by the agent and uncleared.
                let f' = { f with RaisedBy = AgentActor(agentId, "v1"); Clearance = None }
                Ok({ s with Grants = s.Grants.Add(gid, { g with Flags = g.Flags @ [ f' ] }) }, [ GrantFlagged(gid, f') ])
            | ProposeRecipientMatch _ | DraftDossier _ | ProposeReconciliationMatch _ ->
                Ok(s, []) // proposals are advisory; they change no authoritative state

    | Evaluate(gid, policy, mkContext) ->
        match s.Grants.TryFind gid with
        | None -> Error(UnknownGrant gid)
        | Some g when g.State <> Submitted -> Error(InvalidState(gid, g.State, "evaluate"))
        | Some g ->
            let ctx = { mkContext g.Recommendation with AgentFlags = g.Flags }
            let d = decide policy ctx
            let g' = { g with Decisions = g.Decisions @ [ d, ctx.Now ] }
            let ev = evidence (RuleActor(policy.Ref, "decide")) "CTL-grant-decision-record" (string gid) $"%A{d}" ctx.Now (Some policy.Ref)
            match d with
            | Approve(actor, _) ->
                approveGrant { s with Grants = s.Grants.Add(gid, g') } gid g' actor
                |> Result.map (fun (st, evs) -> st, evs @ [ ev ])
            | Refer(flags, _) ->
                let g'' = { g' with State = AwaitingHumanDecision flags; Flags = flags }
                Ok({ s with Grants = s.Grants.Add(gid, g'') }, (flags |> List.map (fun f -> GrantFlagged(gid, f))) @ [ ExceptionCaseOpened(gid, flags); ev ])
            | Deny(reason, _) ->
                Ok({ s with Grants = s.Grants.Add(gid, { g' with State = Declined reason }) }, [ GrantDeclined(gid, reason); ev ])

    | HumanDecide(gid, approver) ->
        match s.Grants.TryFind gid with
        | None -> Error(UnknownGrant gid)
        | Some({ State = AwaitingHumanDecision _ } as g) ->
            let parties = s.Accounts.TryFind g.Recommendation.Account |> Option.map (fun a -> a.Privileged) |> Option.defaultValue Set.empty
            match humanApprove approver parties g.Recommendation.Amount g.Flags with
            | Error e -> Error(HumanDecisionFailed e)
            | Ok(cleared, Approve(actor, _)) ->
                approveGrant { s with Grants = s.Grants.Add(gid, { g with Flags = cleared }) } gid { g with Flags = cleared } actor
                |> Result.map (fun (st, evs) -> st, ExceptionCaseResolved(gid, actor) :: evs)
            | Ok _ -> Error(HumanDecisionFailed NothingToDecide)
        | Some g -> Error(InvalidState(gid, g.State, "human decide"))

    | AttemptApproveAs(gid, actor) ->
        match s.Grants.TryFind gid with
        | None -> Error(UnknownGrant gid)
        | Some _ when not (canApprove actor) -> Error(AgentCannotAuthorize $"%A{actor}")
        | Some g -> Error(InvalidState(gid, g.State, "direct approval bypasses policy"))

    | ReleasePayment(gid, pid, profile, limits, now, secondApprover) ->
        match s.Grants.TryFind gid with
        | None -> Error(UnknownGrant gid)
        | Some g ->
            let r = g.Recommendation
            let paidToday = s.PaidToday.TryFind r.Recipient |> Option.defaultValue 0m
            let failures =
                [ match g.State with
                  | Approved actor when canApprove actor -> ()
                  | st -> yield $"grant not approved by rule or person: %A{st}"
                  if g.Flags |> List.exists (isCleared >> not) then yield "uncleared flags"
                  if profile.Recipient <> r.Recipient then yield "payee profile is for a different recipient"
                  if not profile.Verified then yield "payee profile not verified"
                  match profile.CoolingOffUntil with
                  | Some t when t > now -> yield "payee profile change in cooling-off"
                  | _ -> ()
                  if paidToday + r.Amount > limits.PerRecipientDailyCap then yield "per-recipient daily cap exceeded"
                  if r.Amount > limits.DualControlAbove && secondApprover.IsNone then yield "dual control required"
                  if s.Payments.ContainsKey pid then yield "duplicate payment id" ]
            if not (List.isEmpty failures) then Error(PaymentGateFailed failures)
            else
                let instr =
                    { Id = pid; Grant = gid; Recipient = r.Recipient; Amount = r.Amount; Rail = profile.Rail
                      IdempotencyKey = $"{gid}-{pid}"; GrantIdInRemittance = true }
                let s' = post s (paymentInstructed (nextEntry s) r.Amount)
                Ok({ s' with
                        Grants = s'.Grants.Add(gid, { g with State = Released pid })
                        Payments = s'.Payments.Add(pid, (instr, gid, r.Account))
                        PaidToday = s'.PaidToday.Add(r.Recipient, paidToday + r.Amount) },
                   [ PaymentInstructed instr
                     evidence (RuleActor({ PolicyId = "payment-gate"; Version = 1 }, "gate")) "CTL-payment-gate" (string pid) "all gate checks passed" now None ])

    | SettlePayment(pid, sref) ->
        match s.Payments.TryFind pid with
        | None -> Error(UnknownPayment pid)
        | Some(instr, gid, aid) ->
            let g = s.Grants.[gid]
            match g.State with
            | Released p when p = pid ->
                let s' = post s (paymentSettled (nextEntry s) aid instr.Amount)
                Ok({ s' with Grants = s'.Grants.Add(gid, { g with State = Paid(pid, sref) }) }, [ PaymentSettled(pid, sref) ])
            | st -> Error(InvalidState(gid, st, "settle"))

    | ReturnPayment(pid, code) ->
        match s.Payments.TryFind pid with
        | None -> Error(UnknownPayment pid)
        | Some(instr, gid, aid) ->
            let g = s.Grants.[gid]
            match g.State with
            | Released p when p = pid ->
                let s' = post s (paymentReturned (nextEntry s) aid instr.Amount)
                Ok({ s' with Grants = s'.Grants.Add(gid, { g with State = Returned(pid, code) }) }, [ PaymentReturned(pid, code) ])
            | st -> Error(InvalidState(gid, st, "return"))

/// Run a sequence of commands, stopping at the first rejection.
let run (s0: State) (cmds: Command list) : Result<State * Event list, Rejection * Event list> =
    cmds
    |> List.fold (fun acc cmd ->
        match acc with
        | Error _ -> acc
        | Ok(s, evs) ->
            match handle s cmd with
            | Ok(s', evs') -> Ok(s', evs @ evs')
            | Error e -> Error(e, evs)) (Ok(s0, []))

// ---------- reconciliation (bank/rail statement vs ledger) ----------
type StatementLine = { Reference: string; Amount: Usd }

/// Three-way match of settled payments to bank statement lines by idempotency key.
let reconcile (s: State) (statement: StatementLine list) =
    let expected =
        s.Payments
        |> Map.toList
        |> List.choose (fun (_, (instr, gid, _)) ->
            match s.Grants.[gid].State with
            | Paid _ -> Some(instr.IdempotencyKey, instr.Amount)
            | _ -> None)
        |> Map.ofList
    let seen = statement |> List.map (fun l -> l.Reference, l.Amount) |> Map.ofList
    let missingOnStatement =
        expected |> Map.toList |> List.filter (fun (k, _) -> not (seen.ContainsKey k)) |> List.map (fun (k, a) -> $"paid in ledger, absent on statement: {k} {a}")
    let unexpected =
        statement |> List.filter (fun l -> not (expected.ContainsKey l.Reference)) |> List.map (fun l -> $"on statement, not a settled payment: {l.Reference} {l.Amount}")
    let amountMismatch =
        statement
        |> List.choose (fun l ->
            match expected.TryFind l.Reference with
            | Some a when a <> l.Amount -> Some $"amount mismatch {l.Reference}: ledger {a} statement {l.Amount}"
            | _ -> None)
    missingOnStatement @ unexpected @ amountMismatch

// ---------- reporting (Schedule D Part I style aggregates from the ledger) ----------
type ScheduleDAggregates =
    { Accounts: int
      Contributions: Usd
      GrantsPaid: Usd
      YearEndFundBalances: Usd }

let scheduleD (s: State) (events: Event list) =
    { Accounts = s.Accounts.Count
      Contributions = events |> List.sumBy (function ContributionSettled(_, _, a, _) -> a | _ -> 0m)
      GrantsPaid =
        events |> List.sumBy (function
            | PaymentSettled(pid, _) -> (let (i, _, _) = s.Payments.[pid] in i.Amount)
            | _ -> 0m)
      YearEndFundBalances = s.Accounts |> Map.toList |> List.sumBy (fun (a, _) -> available s a) }
