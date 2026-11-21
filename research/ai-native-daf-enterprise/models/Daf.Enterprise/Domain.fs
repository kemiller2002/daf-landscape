/// Canonical domain types for the AI-native DAF enterprise reference model.
/// Design rule: make illegal states unrepresentable where the type system can do it
/// (an agent cannot clear a flag; a request is not an instruction; money is decimal).
module Daf.Enterprise.Domain

open System

// ---------- identifiers ----------
type PartyId = PartyId of string
type AccountId = AccountId of string
type RecipientId = RecipientId of string
type GrantId = GrantId of string
type PaymentId = PaymentId of string
type PolicyRef = { PolicyId: string; Version: int }
type Ein = Ein of string

/// Amounts in US dollars. Decimal only: no floating point in the ledger.
type Usd = decimal

// ---------- actors ----------
/// Who produced a decision. Agents are a distinct actor kind so that
/// authority rules can refer to them explicitly.
type Actor =
    | RuleActor of PolicyRef * ruleId: string
    | PersonActor of personId: string * authorityRef: string
    | AgentActor of agentId: string * agentVersion: string
    | ExternalActor of system: string

/// Clearance of a flag is a separate type whose constructors exclude agents.
/// DD-005: AI may add a flag, never clear one.
type FlagClearer =
    | ClearedByRule of PolicyRef * ruleId: string
    | ClearedByPerson of personId: string * authorityRef: string

type FlagCode =
    | SanctionsPotentialMatch
    | PossibleProhibitedBenefit
    | PossibleRelatedPartyRecipient
    | NewOrganization
    | ForeignRecipient
    | RequiresExpenditureResponsibility
    | FiscalSponsorIntermediary
    | AmountAboveAutoThreshold
    | StaleEligibilityData
    | PayeeProfileInCoolingOff
    | DiscretionaryPolicyHold
    | UnusualPattern
    | RecipientStatusChanged

type Flag =
    { Code: FlagCode
      RaisedBy: Actor
      Detail: string
      Clearance: FlagClearer option }

// ---------- eligibility facts (bitemporal) ----------
type CharityClass =
    | PublicCharity170b1A          // listed public charity: §4966(c)(1) exception applies
    | Type3NonFunctionallyIntegrated
    | PrivateFoundation
    | ForeignOrganization
    | Other501c3NotPublicCharity
    | NonCharity

type SourceStamp =
    { Source: string          // e.g. "IRS-PUB78", "IRS-EO-BMF", "OFAC-SDN"
      SourceVersion: string   // publication date or list version
      RetrievedAt: DateTime }

type EligibilitySnapshot =
    { Recipient: RecipientId
      Ein: Ein option
      Class: CharityClass
      Revoked: bool
      OfacListed: bool
      RulingYear: int option
      Stamp: SourceStamp }

type Recipient =
    { Id: RecipientId
      LegalName: string
      Ein: Ein option
      IsFiscalSponsor: bool
      RelatedPartyIds: PartyId list }  // parties that control or are employed by the recipient

// ---------- requests vs instructions (DD-003) ----------
type Recognition =
    | FullContact
    | NameOnly
    | Anonymous

/// A donor- or advisor-side request. It has no authority of its own.
type Recommendation =
    { Account: AccountId
      RequestedBy: PartyId
      ViaAgent: string option  // donor-side agent principal, if any (DD-017)
      Recipient: RecipientId
      Amount: Usd
      Purpose: string
      Recognition: Recognition
      IdempotencyKey: string
      SubmittedAt: DateTime }

type Decision =
    | Approve of by: Actor * policy: PolicyRef
    | Refer of flags: Flag list * policy: PolicyRef
    | Deny of reason: string * policy: PolicyRef

/// Grant lifecycle. Approved is reachable only through an approving Decision
/// whose actor is a rule or a person (checked in Policy.fs and Journey.fs).
type GrantState =
    | Submitted
    | AwaitingDonorConfirmation   // agent-originated request above the delegation's confirm_above (INV-A6)
    | AwaitingHumanDecision of Flag list
    | Approved of Actor
    | Declined of string
    | Released of PaymentId
    | Paid of PaymentId * settlementRef: string
    | Returned of PaymentId * returnCode: string
    | Canceled

type Grant =
    { Id: GrantId
      Recommendation: Recommendation
      State: GrantState
      Flags: Flag list
      Decisions: (Decision * DateTime) list }

// ---------- payments ----------
type PaymentProfile =
    { Recipient: RecipientId
      Rail: string
      AccountToken: string
      Verified: bool
      CoolingOffUntil: DateTime option }

type PaymentInstruction =
    { Id: PaymentId
      Grant: GrantId
      Recipient: RecipientId
      Amount: Usd
      Rail: string
      IdempotencyKey: string
      GrantIdInRemittance: bool }

// ---------- agent outputs (Category 2 / 3) ----------
/// The only things an agent can produce. There is deliberately no constructor
/// that approves, releases, clears or writes an authoritative record.
type AgentOutput =
    | ProposeRecipientMatch of RecipientId * confidence: decimal
    | RaiseFlag of Flag
    | DraftDossier of subject: string * text: string
    | ProposeReconciliationMatch of breakId: string * candidate: string

// ---------- evidence ----------
type EvidenceRecord =
    { Subject: string
      Control: string
      Actor: Actor
      Policy: PolicyRef option
      Sources: SourceStamp list
      At: DateTime
      Detail: string }

/// The complete set of tool scopes an agent can ever be granted (INV-A5).
/// There is no constructor for payment, ledger, approval, policy-publish or flag-clearance tools.
type AgentToolScope =
    | ReadScope of resource: string
    | ProposeScope
    | RaiseFlagScope
    | OpenCaseScope
    | DraftScope
    | SendTemplatedScope of templateId: string

/// INV-A8: a causation chain deeper than `limit` with no Rule or Person checkpoint is quarantined.
let mustQuarantine (limit: int) (chain: Actor list) =
    let longestRun =
        chain
        |> List.fold (fun (run, best) a ->
            match a with
            | RuleActor _ | PersonActor _ -> (0, best)
            | AgentActor _ | ExternalActor _ -> (run + 1, max best (run + 1))) (0, 0)
        |> snd
    longestRun > limit

/// Helper: is this actor permitted to make an approving decision?
let canApprove actor =
    match actor with
    | RuleActor _ | PersonActor _ -> true
    | AgentActor _ | ExternalActor _ -> false

let isCleared (flag: Flag) = flag.Clearance.IsSome
