/// Shared value types: ranges, cases and named parameters with their assumption IDs. Pure.
module CompetitiveAdvantageCreation.Domain

open System

/// Numeric range ordered low <= base <= high.
type Range = { Low: float; Base: float; High: float }

/// Which end of a range is the adverse one for the business.
type Adverse =
    | HighIsAdverse
    | LowIsAdverse

/// Scenario case. Favourable takes the favourable end of every range, Adverse the adverse end.
type Case =
    | Favourable
    | BaseCase
    | AdverseCase

let cases = [ Favourable; BaseCase; AdverseCase ]

let caseName c =
    match c with
    | Favourable -> "favourable"
    | BaseCase -> "base"
    | AdverseCase -> "adverse"

let point (x: float) = { Low = x; Base = x; High = x }

/// Value of a range in a case, given which end is adverse.
let pickCase (c: Case) (adv: Adverse) (r: Range) =
    match c, adv with
    | BaseCase, _ -> r.Base
    | Favourable, HighIsAdverse | AdverseCase, LowIsAdverse -> r.Low
    | Favourable, LowIsAdverse | AdverseCase, HighIsAdverse -> r.High

/// Costs, months and shares where more is worse.
let cost c r = pickCase c HighIsAdverse r
/// Revenue, customers and prices where less is worse.
let gain c r = pickCase c LowIsAdverse r

/// A named model parameter read from data/model-inputs/parameters.csv.
type Param =
    { Name: string
      Range: Range
      Unit: string
      Adverse: Adverse
      AllowNegative: bool
      AssumptionIds: string list }

type Params = Map<string, Param>

/// Rejects ranges that are not finite, not ordered low <= base <= high, or negative where negatives are not allowed.
let validateRange (name: string) (allowNegative: bool) (r: Range) : Result<Range, string> =
    let finite = [ r.Low; r.Base; r.High ] |> List.forall (fun x -> not (Double.IsNaN x || Double.IsInfinity x))
    if not finite then Error $"{name}: non-finite value"
    elif not (r.Low <= r.Base && r.Base <= r.High) then Error $"{name}: range not ordered low <= base <= high ({r.Low}, {r.Base}, {r.High})"
    elif not allowNegative && r.Low < 0.0 then Error $"{name}: negative value not allowed ({r.Low})"
    else Ok r

let tryParam (ps: Params) (name: string) : Result<Param, string> =
    match Map.tryFind name ps with
    | Some p -> Ok p
    | None -> Error $"missing parameter '{name}'"

/// Parameter value in a case (orientation taken from the parameter's adverse column).
let pv (ps: Params) (c: Case) (name: string) : float =
    match Map.tryFind name ps with
    | Some p -> pickCase c p.Adverse p.Range
    | None -> failwithf "missing parameter '%s' (inputs are validated before models run)" name

/// Replace one parameter's range (used by tornado, Monte Carlo and stress transforms).
let withRange (name: string) (r: Range) (ps: Params) : Params =
    match Map.tryFind name ps with
    | Some p -> Map.add name { p with Range = r } ps
    | None -> ps

/// Fix every parameter at its value in a case (point ranges).
let atCase (c: Case) (ps: Params) : Params =
    ps |> Map.map (fun _ p -> { p with Range = point (pickCase c p.Adverse p.Range) })

/// Applicative collection: all Ok or every error.
let collect (rs: Result<'T, string> list) : Result<'T list, string list> =
    let errs = rs |> List.choose (function Error e -> Some e | Ok _ -> None)
    if List.isEmpty errs then Ok(rs |> List.choose (function Ok x -> Some x | Error _ -> None)) else Error errs

let money (x: float) =
    let inv = Globalization.CultureInfo.InvariantCulture
    let a = abs x
    let s =
        if a >= 1e6 then (a / 1e6).ToString("0.00", inv) + "M"
        elif a >= 1e3 then (a / 1e3).ToString("0", inv) + "k"
        else a.ToString("0", inv)
    if Double.IsInfinity x || Double.IsNaN x then "n/a"
    elif x < 0.0 && s <> "0" then "-$" + s
    else "$" + s

let num0 (x: float) = x.ToString("0", Globalization.CultureInfo.InvariantCulture)
let num1 (x: float) = x.ToString("0.0", Globalization.CultureInfo.InvariantCulture)
let num2 (x: float) = x.ToString("0.00", Globalization.CultureInfo.InvariantCulture)
let pct (x: float) = (x * 100.0).ToString("0", Globalization.CultureInfo.InvariantCulture) + "%"
let monthStr (m: int option) = match m with Some v -> string v | None -> "none in 120"
