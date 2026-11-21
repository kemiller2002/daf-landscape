module Daf.Enterprise.Tests.Fixtures

open System
open System.IO
open Daf.Enterprise.Domain
open Daf.Enterprise.Policy

let now = DateTime(2026, 11, 20, 12, 0, 0, DateTimeKind.Utc)

let policy =
    { Ref = { PolicyId = "grant-policy"; Version = 3 }
      AutoApproveLimit = 250000m           // matches 08-governance-and-compliance thresholds [A]
      EligibilityFreshness = TimeSpan.FromDays 35.0
      NewOrgYears = 2
      DiscretionaryHolds = Set.empty
      ApprovedBy = "board-resolution-2026-11" }

let stamp days = { Source = "IRS-PUB78"; SourceVersion = "2026-11"; RetrievedAt = now.AddDays(-days) }

let donor = PartyId "P-donor"
let account = AccountId "A-1"
let recipientId = RecipientId "R-food-bank"

let recipient =
    { Id = recipientId; LegalName = "Example Food Bank"; Ein = Some(Ein "12-3456789")
      IsFiscalSponsor = false; RelatedPartyIds = [] }

let eligible =
    { Recipient = recipientId; Ein = Some(Ein "12-3456789"); Class = PublicCharity170b1A
      Revoked = false; OfacListed = false; RulingYear = Some 1985; Stamp = stamp 3.0 }

let recommendation amount key =
    { Account = account; RequestedBy = donor; ViaAgent = None; Recipient = recipientId
      Amount = amount; Purpose = "general support"; Recognition = FullContact
      IdempotencyKey = key; SubmittedAt = now }

let context r =
    { Now = now; Recommendation = r; Recipient = recipient; Eligibility = Some eligible
      AccountParties = Set.singleton donor; AgentFlags = [] }

let complianceOfficer =
    { PersonId = "S-grants-1"; Roles = set [ GrantsCompliance ]; AuthorityLimit = 1000000m
      RelatedParties = Set.empty; AuthorityRef = "DOA-2026-GC-1" }

let sanctionsOfficer =
    { PersonId = "S-sanctions-1"; Roles = set [ SanctionsOfficer; GrantsCompliance ]; AuthorityLimit = 5000000m
      RelatedParties = Set.empty; AuthorityRef = "DOA-2026-SO-1" }

/// Repository root (directory containing .git), found by walking up from the test binary.
let repoRoot () =
    let rec up (d: DirectoryInfo) =
        if isNull d then failwith "repository root not found"
        elif Directory.Exists(Path.Combine(d.FullName, ".git")) then d.FullName
        else up d.Parent
    up (DirectoryInfo AppContext.BaseDirectory)

let workstream () = Path.Combine(repoRoot (), "research", "ai-native-daf-enterprise")

/// Minimal RFC-4180 CSV reader (quoted fields, embedded commas); pure over the text.
let parseCsv (text: string) : string list list =
    let rec fields (chars: char list) (field: char list) (acc: string list) (inQuotes: bool) =
        match chars, inQuotes with
        | [], _ -> List.rev (String(field |> List.rev |> Array.ofList) :: acc)
        | '"' :: '"' :: rest, true -> fields rest ('"' :: field) acc true
        | '"' :: rest, true -> fields rest field acc false
        | '"' :: rest, false when List.isEmpty field -> fields rest field acc true
        | ',' :: rest, false -> fields rest [] (String(field |> List.rev |> Array.ofList) :: acc) false
        | c :: rest, _ -> fields rest (c :: field) acc inQuotes
    text.Replace("\r\n", "\n").Split('\n')
    |> Array.filter (fun l -> l.Trim() <> "")
    |> Array.map (fun l -> fields (List.ofSeq l) [] [] false)
    |> List.ofArray

let readCsv relPath =
    let rows = File.ReadAllText(Path.Combine(workstream (), relPath)) |> parseCsv
    let header = List.head rows
    rows |> List.tail |> List.map (fun r -> List.zip header (r |> List.truncate header.Length) |> Map.ofList)
