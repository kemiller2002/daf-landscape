/// E7/E11 — Economics of a cross-sponsor verification network and other infrastructure business models.
/// Uses the MEASURED reuse curve from public FY2023 Schedule I data (data/workflow-innovation/recipient-overlap-summary.csv);
/// every money parameter is an assumption [A].
module Daf.Experiments.NetworkEconomics

open System
open System.IO

type CurvePoint = { Order: string; K: int; SponsorEin: string; RecipientShare: float }
type SponsorRow = { Ein: string; Rank: int; DistinctRecipients: float }

/// Minimal CSV split honoring quotes (pure).
let splitCsv (line: string) =
    let rec go (cs: char list) (cur: char list) (acc: string list) inQ =
        match cs, inQ with
        | [], _ -> List.rev (String(List.rev cur |> Array.ofList) :: acc)
        | '"' :: '"' :: rest, true -> go rest ('"' :: cur) acc true
        | '"' :: rest, _ -> go rest cur acc (not inQ)
        | ',' :: rest, false -> go rest [] (String(List.rev cur |> Array.ofList) :: acc) false
        | c :: rest, _ -> go rest (c :: cur) acc inQ
    go (List.ofSeq line) [] [] false |> Array.ofList

let load (path: string) =
    let rows = File.ReadAllLines path |> Array.tail |> Array.map splitCsv
    // columns: section,scope,order,k,sponsor_ein,sponsor_rank,sponsor_name,fiscal_year,bucket,metric,value,definition
    let curve =
        rows |> Array.choose (fun r ->
            if r.[0] = "reuse_curve" && r.[9] = "recipient_share" then
                Some { Order = r.[2]; K = int r.[3]; SponsorEin = r.[4]; RecipientShare = float r.[10] }
            else None) |> List.ofArray
    let sponsors =
        rows |> Array.choose (fun r ->
            if r.[0] = "sponsor" && r.[9] = "distinct_recipients" then
                Some { Ein = r.[4]; Rank = int r.[5]; DistinctRecipients = float r.[10] }
            else None) |> List.ofArray
    curve, sponsors

type Params =
    { HumanDeterminationShare: float  // share of a sponsor's distinct recipients needing human judgment (core proxy ~7.76% of lines, EV-079) [A as per-recipient]
      CostPerDetermination: float     // loaded human cost per determination [A]: 45 min at $90/h
      PayeeVerificationCost: float    // bank-account verification + callback per recipient [A]
      OperatorFixedCost: float        // neutral network operator, per year [A]
      FeeShareOfSavings: float }      // price as share of member savings [A]

let defaults = { HumanDeterminationShare = 0.08; CostPerDetermination = 67.5; PayeeVerificationCost = 15.0; OperatorFixedCost = 1200000.0; FeeShareOfSavings = 0.4 }

type JoinResult =
    { Order: string
      K: int
      MemberSavings: float          // annual savings for the k-th joiner
      CumulativeOperatorRevenue: float
      OperatorBreakEven: bool }

let valuePerReusedRecipient (p: Params) = p.HumanDeterminationShare * p.CostPerDetermination + p.PayeeVerificationCost

let joinCurve (p: Params) (curve: CurvePoint list) (sponsors: SponsorRow list) (order: string) =
    let size = sponsors |> List.map (fun s -> s.Ein, s.DistinctRecipients) |> Map.ofList
    curve
    |> List.filter (fun c -> c.Order = order)
    |> List.sortBy (fun c -> c.K)
    |> List.fold (fun (acc: JoinResult list, cum) c ->
        let n = size.TryFind c.SponsorEin |> Option.defaultValue 0.0
        let savings = n * c.RecipientShare * valuePerReusedRecipient p
        let cum' = cum + savings * p.FeeShareOfSavings
        (acc @ [ { Order = order; K = c.K; MemberSavings = savings; CumulativeOperatorRevenue = cum'; OperatorBreakEven = cum' >= p.OperatorFixedCost } ], cum')) ([], 0.0)
    |> fst

/// Random order is reported as a mean curve without sponsor identity; value it with mean sponsor size.
let joinCurveRandom (p: Params) (curve: CurvePoint list) (sponsors: SponsorRow list) =
    let meanSize = sponsors |> List.averageBy (fun s -> s.DistinctRecipients)
    curve
    |> List.filter (fun c -> c.Order = "random_mean_200")
    |> List.sortBy (fun c -> c.K)
    |> List.fold (fun (acc: JoinResult list, cum) c ->
        let savings = meanSize * c.RecipientShare * valuePerReusedRecipient p
        let cum' = cum + savings * p.FeeShareOfSavings
        (acc @ [ { Order = "random_mean_200"; K = c.K; MemberSavings = savings; CumulativeOperatorRevenue = cum'; OperatorBreakEven = cum' >= p.OperatorFixedCost } ], cum')) ([], 0.0)
    |> fst

let firstBreakEven (rows: JoinResult list) = rows |> List.tryFind (fun r -> r.OperatorBreakEven) |> Option.map (fun r -> r.K)

// ---------------- E11: infrastructure business models (per-unit economics, all [A]) ----------------
type ModelEcon =
    { Model: string
      Customers: int
      Revenue: float
      Cost: float
      Note: string }

/// Grantmaking infrastructure platform: per-grant decision + eligibility + payment orchestration fee.
let grantInfrastructure customers grantsPerCustomer feePerGrant =
    let grants = float customers * grantsPerCustomer
    { Model = "grantmaking infrastructure (per-grant API)"; Customers = customers; Revenue = grants * feePerGrant
      Cost = 2500000.0 + float customers * 40000.0 + grants * 0.05
      Note = "fixed $2.5m platform team [A]; $40k per customer support [A]; $0.05 compute+data per grant [A]" }

/// Shared compliance provider: policy packs, obligation monitoring, evidence; subscription per sponsor.
let sharedCompliance customers subscription =
    { Model = "shared compliance policy packs"; Customers = customers; Revenue = float customers * subscription
      Cost = 1800000.0 + float customers * 15000.0
      Note = "counsel + policy engineers $1.8m [A]; $15k per sponsor onboarding/support [A]" }
