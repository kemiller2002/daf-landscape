// Run: copy daf-landscape/research/commercial-opportunity/servicing-economics/model/src/ServicingEconomics/bin/Release/net10.0/ServicingEconomics.dll here, then dotnet fsi <script>.fsx
#r "ServicingEconomics.dll"
open ServicingEconomics.Domain
open ServicingEconomics.Economics
open ServicingEconomics.Parameters
open ServicingEconomics.Analysis
let shapeOf n b = equalSponsors n (sponsor "sponsor" 1000.0 b)
let withExtra (extra: float) = { modelB with NonPersonnelFixed = modelB.NonPersonnelFixed @ [ ("layer extras", extra) ] }
let be org ap n b target =
    let shape = shapeOf n b
    assetsForMargin (fun sp -> evaluate org sponsorActivities ap (price 20.0) noStress sp) shape target
let fmt = function Some (a: float) -> sprintf "%.2fB" (a/1e9) | None -> "not<=20B"
for name, extra in ["fixed-extras-low",606191.0; "fixed-extras-base",2068765.0; "fixed-extras-high",5511729.0; "base-without-echelon-A",2068765.0-433670.0] do
  for b in [150000.0; 300000.0; 500000.0] do
    printfn "%s|bal=%.0f|BE=%s|20pct=%s" name b (fmt (snd (be (withExtra extra) AiNative 5 b 0.0))) (fmt (snd (be (withExtra extra) AiNative 5 b 0.2)))
