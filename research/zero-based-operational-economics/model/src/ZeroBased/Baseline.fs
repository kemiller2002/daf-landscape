/// Reproduction of the original competitive-displacement model (preserved comparison baseline).
/// Calls the baseline code directly; nothing is re-implemented.
module ZeroBased.Baseline

open CompetitiveDisplacement.Inputs
open CompetitiveDisplacement.Events
open CompetitiveDisplacement.Enterprise

type Reconstruction =
    { ModeId: string
      BreakEvenAssets: float
      FullyLoadedAssets: float
      Accounts: float
      OpexAtBreakEven: float
      Fixed: float
      SponsorLevel: float
      VariablePerAcct: float
      VariableTotal: float
      LabourPerAcct: float
      InfraPerAcct: float
      ExternalPerAcct: float
      AiPerAcct: float
      PreventionPerAcct: float
      FailurePerAcct: float
      HumanMinutesPerAcct: float
      Build: float }

let reconstruct (inputs: CompetitiveDisplacement.Inputs.Inputs) (modeId: string) (bps: float) : Reconstruction =
    let vals = CompetitiveDisplacement.Analysis.baseVals inputs
    let mode = inputs.Modes |> List.find (fun m -> m.Id = modeId)
    let m = economics Base vals inputs.Events mode
    let balance = v vals "avg_balance"
    let sponsors = v vals "sponsors"
    let a = breakEvenAssets bps balance sponsors m |> Option.defaultValue infinity
    let loaded = breakEvenAssetsLoaded bps balance sponsors m |> Option.defaultValue infinity
    let accts = a / balance
    let share = mode.VendorEventShare
    let sumBy (f: CompetitiveDisplacement.Events.EventCost -> float) = (m.Events |> List.sumBy f) * share
    { ModeId = modeId
      BreakEvenAssets = a
      FullyLoadedAssets = loaded
      Accounts = accts
      OpexAtBreakEven = m.VendorFixed + sponsors * m.VendorSponsorLevelCost + accts * m.VendorVariablePerAcct
      Fixed = m.VendorFixed
      SponsorLevel = sponsors * m.VendorSponsorLevelCost
      VariablePerAcct = m.VendorVariablePerAcct
      VariableTotal = accts * m.VendorVariablePerAcct
      LabourPerAcct = sumBy (fun c -> c.LabourPerAcct)
      InfraPerAcct = (if mode.OwnsPlatform then v vals "infra_per_account_owned" else v vals "software_per_account_licensed")
      ExternalPerAcct = sumBy (fun c -> c.VendorExternalPerAcct)
      AiPerAcct = sumBy (fun c -> c.AiPerAcct)
      PreventionPerAcct = sumBy (fun c -> c.PreventionPerAcct)
      FailurePerAcct = sumBy (fun c -> c.ExpectedFailurePerAcct)
      HumanMinutesPerAcct = m.HumanMinutesPerAcct
      Build = m.Build }

/// Baseline annual vendor opex for a mode at a given account count (for like-for-like comparison).
let opexAt (inputs: CompetitiveDisplacement.Inputs.Inputs) (modeId: string) (accounts: float) (sponsors: float) =
    let vals = CompetitiveDisplacement.Analysis.baseVals inputs
    let mode = inputs.Modes |> List.find (fun m -> m.Id = modeId)
    let m = economics Base vals inputs.Events mode
    m.VendorFixed + sponsors * m.VendorSponsorLevelCost + accounts * m.VendorVariablePerAcct

let loadBaseline (dir: string) = CompetitiveDisplacement.Program.loadInputs dir
