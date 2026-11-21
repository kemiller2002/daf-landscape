/// Append-only double-entry ledger derived from business events (DD-006).
/// Balances are a fold over the journal; corrections are reversing entries.
module Daf.Enterprise.Ledger

open Daf.Enterprise.Domain

type LedgerAccount =
    | CashAtCustodian
    | CashInTransit                    // payment instructed, not yet settled
    | FundBalance of AccountId         // the donor-advised fund's net assets
    | GrantsPayable of AccountId       // approved grants not yet released
    | Suspense                         // received, not yet attributable

type Posting = { Account: LedgerAccount; Debit: Usd; Credit: Usd }

type JournalEntry =
    { EntryId: int
      SourceEvent: string
      Postings: Posting list }

let isBalanced (e: JournalEntry) =
    let d = e.Postings |> List.sumBy (fun p -> p.Debit)
    let c = e.Postings |> List.sumBy (fun p -> p.Credit)
    d = c && d > 0m

let dr acct amt = { Account = acct; Debit = amt; Credit = 0m }
let cr acct amt = { Account = acct; Debit = 0m; Credit = amt }

/// Natural-sign balance: assets are debit-positive, fund balances and payables credit-positive.
let balance (journal: JournalEntry list) (acct: LedgerAccount) : Usd =
    let raw =
        journal
        |> List.collect (fun e -> e.Postings)
        |> List.filter (fun p -> p.Account = acct)
        |> List.sumBy (fun p -> p.Debit - p.Credit)
    match acct with
    | CashAtCustodian | CashInTransit -> raw
    | FundBalance _ | GrantsPayable _ | Suspense -> -raw

/// Accounting identity: assets = fund balances + payables + suspense.
let identityHolds (journal: JournalEntry list) =
    let accounts = journal |> List.collect (fun e -> e.Postings |> List.map (fun p -> p.Account)) |> List.distinct
    let assets = [ CashAtCustodian; CashInTransit ] |> List.sumBy (balance journal)
    let claims =
        accounts
        |> List.filter (function FundBalance _ | GrantsPayable _ | Suspense -> true | _ -> false)
        |> List.sumBy (balance journal)
    assets = claims

// Posting rules (versioned in a real system; v1 here).
let contributionSettled entryId account amount =
    { EntryId = entryId; SourceEvent = "ContributionSettled"
      Postings = [ dr CashAtCustodian amount; cr (FundBalance account) amount ] }

let grantApproved entryId account amount =
    { EntryId = entryId; SourceEvent = "GrantApproved"
      Postings = [ dr (FundBalance account) amount; cr (GrantsPayable account) amount ] }

/// Cash leaves the operating account for the rail; the obligation stays until settlement.
let paymentInstructed entryId amount =
    { EntryId = entryId; SourceEvent = "PaymentInstructed"
      Postings = [ dr CashInTransit amount; cr CashAtCustodian amount ] }

/// Settlement extinguishes the payable.
let paymentSettled entryId account amount =
    { EntryId = entryId; SourceEvent = "PaymentSettled"
      Postings = [ dr (GrantsPayable account) amount; cr CashInTransit amount ] }

/// A returned payment brings cash back and restores the fund balance.
let paymentReturned entryId account amount =
    { EntryId = entryId; SourceEvent = "PaymentReturned"
      Postings =
        [ dr CashAtCustodian amount; cr CashInTransit amount
          dr (GrantsPayable account) amount; cr (FundBalance account) amount ] }
