module CompetitiveDisplacement.Tests

open System.IO
open Xunit
open CompetitiveDisplacement
open CompetitiveDisplacement.Inputs

let inputsDir = Path.Combine(__SOURCE_DIRECTORY__, "../../../data/model-inputs")
let inputs =
    match Program.loadInputs inputsDir with
    | Ok i -> i
    | Error es -> failwithf "inputs: %A" es

let vals = Analysis.baseVals inputs
let econ id = Enterprise.economics Base vals inputs.Events (Analysis.modeById inputs id)
let close (tol: float) (e: float) (a: float) = Assert.True(abs (e - a) <= tol, $"expected {e}, got {a}")

[<Fact>]
let ``CSV parser honours quotes, escaped quotes and embedded commas`` () =
    let _, rows = Csv.parse "a,b\n\"x, y\",\"say \"\"hi\"\"\"\n"
    Assert.Equal("x, y", rows.Head.["a"])
    Assert.Equal("say \"hi\"", rows.Head.["b"])

[<Fact>]
let ``All inputs parse: 25 events, 7 modes, 10 registry components`` () =
    Assert.Equal(25, inputs.Events.Length)
    Assert.Equal(7, inputs.Modes.Length)
    Assert.Equal(10, inputs.Components.Length)

[<Fact>]
let ``Registry components reconstruct the published 316k estimate`` () =
    let _, total = Registry.reconstruction Base inputs.Components
    close 1000.0 316000.0 total

[<Fact>]
let ``Human minutes fall monotonically from conventional to AI-native`` () =
    let m id = (econ id).HumanMinutesPerAcct
    Assert.True(m "MD-1" > m "MD-2" && m "MD-2" > m "MD-3" && m "MD-3" > m "MD-4" && m "MD-4" > m "MD-5")

[<Fact>]
let ``AI-native minutes stay within the plausible band around PR 87's ~30 minutes (REV2 field AI factor)`` () =
    let m = (econ "MD-5").HumanMinutesPerAcct
    Assert.InRange(m, 12.0, 60.0)

[<Fact>]
let ``A weaker AI factor makes AI-native dearer and leaves exception-driven unchanged (REV2 direction fix)`` () =
    let weak = Map.add "ai_assist_duration_factor" 0.97 vals
    let e id vs = (Enterprise.economics Base vs inputs.Events (Analysis.modeById inputs id)).HumanMinutesPerAcct
    Assert.True(e "MD-5" weak > e "MD-5" vals)
    close 1e-9 (e "MD-4" vals) (e "MD-4" weak)

[<Fact>]
let ``Fully loaded break-even exceeds operating break-even`` () =
    let m = econ "MD-5"
    let a = Enterprise.breakEvenAssets 20.0 250000.0 5.0 m |> Option.get
    let l = Enterprise.breakEvenAssetsLoaded 20.0 250000.0 5.0 m |> Option.get
    Assert.True(l > a)

[<Fact>]
let ``Route capital is non-negative and churn lowers live customers`` () =
    let r = inputs.Routes |> List.find (fun r -> r.Id = "ER-7")
    let rv = Routes.valuesAt Base r
    let withChurn = Routes.simulate r rv
    let noChurn = Routes.simulate { r with Churn = 0.0 } rv
    Assert.True(withChurn.Capital >= 0.0)
    Assert.True(withChurn.CustomersAt60 < noChurn.CustomersAt60)

[<Fact>]
let ``Profit is zero at the break-even assets`` () =
    let m = econ "MD-5"
    match Enterprise.breakEvenAssets 20.0 250000.0 5.0 m with
    | Some a ->
        let profit = a * 0.002 - (m.VendorFixed + 5.0 * m.VendorSponsorLevelCost + a / 250000.0 * m.VendorVariablePerAcct)
        close 1.0 0.0 profit
    | None -> failwith "expected a break-even"

[<Fact>]
let ``Break-even assets fall as the fee rises`` () =
    let m = econ "MD-5"
    let xs = Analysis.bpsGrid |> List.map (fun b -> Enterprise.breakEvenAssets b 250000.0 5.0 m |> Option.defaultValue infinity)
    Assert.True(xs |> List.pairwise |> List.forall (fun (a, b) -> b <= a))

[<Fact>]
let ``Licensing shifts labour to a less efficient sponsor: system cost rises, vendor cost falls (REV2)`` () =
    Assert.True((econ "MD-6").SystemVariablePerAcct > (econ "MD-5").SystemVariablePerAcct)
    Assert.True((econ "MD-6").VendorVariablePerAcct < (econ "MD-5").VendorVariablePerAcct)

[<Fact>]
let ``Prevention never increases event cost when its own cost is below the avoided work`` () =
    let rows = Analysis.preventionVsSpeed inputs vals
    Assert.True(rows |> List.sumBy (fun r -> r.PreventionValue) > 0.0)

[<Fact>]
let ``Change-driven registry is cheaper than 180-day full re-review`` () =
    let alt = inputs.Alts |> List.find (fun a -> a.Id = "RA-3")
    let rp = Analysis.registryVals inputs Base
    let d r = { Registry.CharitiesPerSponsor = 20000.0; Registry.Sponsors = 1.0; Registry.ChangeRate = 0.04; Registry.RefreshDays = r; Registry.GrantsPerYear = 70000.0 }
    Assert.True((Registry.cost alt rp (d None)).Total < (Registry.cost alt rp (d (Some 180.0))).Total)

[<Fact>]
let ``Triangular samples stay in range and percentiles are ordered`` () =
    let r = { Low = 1.0; Base = 2.0; High = 5.0 }
    let xs = [ 0.0; 0.1; 0.5; 0.9; 0.999 ] |> List.map (Sampling.triangular r)
    Assert.True(xs |> List.forall (fun x -> x >= 1.0 && x <= 5.0))
    Assert.True(Sampling.percentile 0.1 xs <= Sampling.percentile 0.9 xs)

[<Fact>]
let ``Outputs are deterministic`` () =
    Assert.Equal<(string * string) list>(Program.outputs inputs, Program.outputs inputs)

[<Fact>]
let ``Validator reports duplicate ids, unknown sources and broken links`` () =
    let csv = "source_id,title\nSRC-001,a\nSRC-001,b\n"
    let claims = "claim_id,status,source_ids\nCLM-001,confirmed,SRC-999\n"
    let fs = { Validate.Csvs = [ "/r/data/registers/sources.csv", csv; "/r/data/registers/claims.csv", claims ]
               Validate.Markdown = [ "/r/00-executive-summary.md", "[x](missing.md)" ]
               Validate.Exists = fun _ -> false }
    let errs = Validate.validate "/r" fs
    Assert.Contains(errs, fun e -> e.Contains "duplicate id SRC-001")
    Assert.Contains(errs, fun e -> e.Contains "unknown source reference SRC-999")
    Assert.Contains(errs, fun e -> e.Contains "broken link missing.md")
