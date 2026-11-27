/// Annual workload per activity, split between vendor (Echelon/Unbound), sponsor and external parties. Pure.
module ZeroBased.Workload

open CompetitiveDisplacement.Inputs
open ZeroBased.Domain
open ZeroBased.Volume

type Load =
    { Activity: Activity
      Bucket: Bucket
      Events: float
      AutoEvents: float
      HumanEvents: float
      AuthorizedEvents: float
      /// Human minutes of the primary handler (after AI factor where applicable).
      Minutes: float
      /// Second-person minutes for independent authorization.
      AuthMinutes: float
      VendorShare: float
      ExternalCost: float }

/// AI preparation shortens a touch only where the activity is classified AI-assisted.
let aiFactor (vals: Values) (a: Activity) =
    if a.Classification = "AI-ASSISTED" then v vals "ai_assist_duration_factor" else 1.0

let load (level: Level) (vals: Values) (cfg: Config) (c: Counts) (a: Activity) : Load =
    let b = bucket a
    let events = pick level a.Freq * driverUnits c a.Driver
    let exceptionRate = min 1.0 (pick level a.Exception * (if a.Exception.Base >= 1.0 then 1.0 else v vals "exception_mult"))
    let human = events * exceptionRate
    let minutes = human * pick level a.Minutes * v vals "duration_mult" * aiFactor vals a
    let authorized = if a.Independent then human else 0.0
    let authMinutes = authorized * pick level a.Minutes * v vals "independent_review_share"
    { Activity = a
      Bucket = b
      Events = events
      AutoEvents = events - human
      HumanEvents = human
      AuthorizedEvents = authorized
      Minutes = minutes
      AuthMinutes = authMinutes
      VendorShare = Map.tryFind b cfg.Shares |> Option.defaultValue 0.0
      ExternalCost = events * a.ExternalCost }

let loads level vals cfg counts (acts: Activity list) = acts |> List.map (load level vals cfg counts)

/// Hours by role borne by a party. Vendor hours use the config share; sponsor hours the remainder.
/// Independent-authorization second-person minutes are assigned to the "authorizer" role.
let hoursByRole (vendor: bool) (ls: Load list) : Map<string, float> =
    let share (l: Load) = if vendor then l.VendorShare else 1.0 - l.VendorShare
    let primary = ls |> List.map (fun l -> l.Activity.Role, l.Minutes * share l / 60.0)
    let auth = ls |> List.map (fun l -> "authorizer", l.AuthMinutes * share l / 60.0)
    primary @ auth
    |> List.filter (fun (r, h) -> h > 0.0 && r <> "none" && r <> "")
    |> List.groupBy fst
    |> List.map (fun (r, xs) -> r, xs |> List.sumBy snd)
    |> Map.ofList

type Totals =
    { Events: float
      AutoEvents: float
      HumanEvents: float
      AuthorizedEvents: float
      HumanHours: float
      VendorHours: float
      SponsorHours: float
      ExternalCost: float
      AutoShare: float }

let totals (ls: Load list) : Totals =
    let ev = ls |> List.sumBy (fun l -> l.Events)
    let auto = ls |> List.sumBy (fun l -> l.AutoEvents)
    let hrs (f: Load -> float) = ls |> List.sumBy (fun l -> (l.Minutes + l.AuthMinutes) * f l / 60.0)
    { Events = ev
      AutoEvents = auto
      HumanEvents = ls |> List.sumBy (fun l -> l.HumanEvents)
      AuthorizedEvents = ls |> List.sumBy (fun l -> l.AuthorizedEvents)
      HumanHours = hrs (fun _ -> 1.0)
      VendorHours = hrs (fun l -> l.VendorShare)
      SponsorHours = hrs (fun l -> 1.0 - l.VendorShare)
      ExternalCost = ls |> List.sumBy (fun l -> l.ExternalCost)
      AutoShare = if ev > 0.0 then auto / ev else 1.0 }
