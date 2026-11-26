/// Model 6: shared infrastructure allocation across products and economic entities. The allocation rule is an explicit
/// input (echelon-organization-administration strategy/daf-entry/02: costs of the five entities are not combined
/// without a stated rule). Allocation conserves totals by construction and is tested. Pure.
module CompetitiveAdvantageCreation.SharedInfra

open CompetitiveAdvantageCreation.Cashflow

type Pool = { Id: string; Name: string; Annual: float }

type Product =
    { Id: string
      Name: string
      Entity: Entity
      /// Driver values, keyed by rule name ("usage", "revenue", "standalone", "equal").
      Drivers: Map<string, float>
      RevenueBearing: bool }

type Rule =
    | Equal
    | Usage
    | Revenue
    | Standalone

let parseRule (s: string) =
    match s.Trim().ToLowerInvariant() with
    | "equal" -> Ok Equal
    | "usage" -> Ok Usage
    | "revenue" -> Ok Revenue
    | "standalone" -> Ok Standalone
    | x -> Error $"unknown allocation rule '{x}'"

let ruleName r =
    match r with
    | Equal -> "equal"
    | Usage -> "usage"
    | Revenue -> "revenue"
    | Standalone -> "standalone"

type Allocation = { PoolId: string; ProductId: string; Entity: Entity; Amount: float; Weight: float }

/// Weights for a rule. A product that bears no revenue gets no revenue-rule weight; if no product has a positive
/// driver the whole pool falls on the designated owner product (no cost disappears).
let weights (rule: Rule) (owner: string) (products: Product list) : (string * float) list =
    let raw =
        products
        |> List.map (fun p ->
            let w =
                match rule with
                | Equal -> 1.0
                | Usage -> Map.tryFind "usage" p.Drivers |> Option.defaultValue 0.0
                | Revenue -> if p.RevenueBearing then Map.tryFind "revenue" p.Drivers |> Option.defaultValue 0.0 else 0.0
                | Standalone -> Map.tryFind "standalone" p.Drivers |> Option.defaultValue 0.0
            p.Id, max 0.0 w)
    let total = raw |> List.sumBy snd
    if total > 0.0 then raw |> List.map (fun (id, w) -> id, w / total)
    else products |> List.map (fun p -> p.Id, (if p.Id = owner then 1.0 else 0.0))

let allocate (rule: Rule) (owner: string) (products: Product list) (pools: Pool list) : Allocation list =
    let ws = weights rule owner products
    [ for pool in pools do
          for p in products do
              let w = ws |> List.find (fun (id, _) -> id = p.Id) |> snd
              { PoolId = pool.Id; ProductId = p.Id; Entity = p.Entity; Amount = pool.Annual * w; Weight = w } ]

/// Sum by entity. Combining entities requires an explicit, named justification (otherwise an error).
let byEntity (allocs: Allocation list) = allocs |> List.groupBy (fun a -> a.Entity) |> List.map (fun (e, xs) -> e, xs |> List.sumBy (fun a -> a.Amount)) |> List.sortBy (fun (e, _) -> entityCode e)

let combineEntities (justification: string option) (entities: Entity list) (allocs: Allocation list) : Result<float, string> =
    match justification with
    | Some j when j.Trim() <> "" -> Ok(allocs |> List.filter (fun a -> List.contains a.Entity entities) |> List.sumBy (fun a -> a.Amount))
    | _ when List.length (List.distinct entities) <= 1 -> Ok(allocs |> List.filter (fun a -> List.contains a.Entity entities) |> List.sumBy (fun a -> a.Amount))
    | _ -> Error "combining economic entities needs an explicit, recorded justification"

/// The share of shared cost a product bears, i.e. the S7 multiplier implied by the rule (agent AB assumed 0.6).
let shareOf (productId: string) (allocs: Allocation list) (pools: Pool list) =
    let total = pools |> List.sumBy (fun p -> p.Annual)
    if total = 0.0 then 0.0 else (allocs |> List.filter (fun a -> a.ProductId = productId) |> List.sumBy (fun a -> a.Amount)) / total
