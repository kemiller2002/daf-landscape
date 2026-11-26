// Run: copy daf-landscape/research/commercial-opportunity/servicing-economics/model/src/ServicingEconomics/bin/Release/net10.0/ServicingEconomics.dll here, then dotnet fsi <script>.fsx
#r "ServicingEconomics.dll"
open ServicingEconomics.Domain
open ServicingEconomics.Economics
open ServicingEconomics.Parameters
open ServicingEconomics.Analysis
let shapeOf n b = equalSponsors n (sponsor "sponsor" 1000.0 b)
let show name (r: Result) =
    printfn "%s|acc=%.0f|sp=%d|rev=%.0f|ext=%.0f|hours=%.0f|coreH=%.0f|addedFte=%.1f|addedCost=%.0f|peak=%.0f|corePers=%.0f|nonPers=%.0f|step=%.0f|sponsorCosts=%.0f|total=%.0f|profit=%.0f" name r.Accounts r.Sponsors r.Revenue r.ExternalVariableCost r.ServicingHours r.CoreServicingHours r.AddedServicingFte r.AddedServicingCost r.PeakCost r.CorePersonnel r.NonPersonnelFixed r.StepFixed r.SponsorCosts r.TotalCost r.OperatingProfit
let s5 = (shapeOf 5 150000.0).Build 1.5e9
for ap, n in [AiNative,"ainative"; AiEnhanced,"aienh"; Conventional,"conv"; AiNativeWithElimination,"elim"] do
  show ("R-modelB-"+n) (evaluate modelB sponsorActivities ap (price 20.0) noStress s5)
show "R-modelB-ainative-min0.35" (evaluate modelB sponsorActivities AiNative (price 20.0) {noStress with MinutesFactor = minutesLowFactor} s5)
show "R-modelB-ainative-min3.33" (evaluate modelB sponsorActivities AiNative (price 20.0) {noStress with MinutesFactor = minutesHighFactor} s5)
show "R-modelB-ainative-min2.0" (evaluate modelB sponsorActivities AiNative (price 20.0) {noStress with MinutesFactor = 2.0} s5)
show "R-modelB-ainative-exc1.5" (evaluate modelB sponsorActivities AiNative (price 20.0) {noStress with VolumeFactor = 1.5} s5)
show "R-modelB-ainative-vendor1.5" (evaluate modelB sponsorActivities AiNative (price 20.0) {noStress with VendorFactor = 1.5} s5)
show "R-modelB-ainative-wage1.15" (evaluate modelB sponsorActivities AiNative (price 20.0) {noStress with WageFactor = 1.15} s5)
show "R-modelB-ainative-incident1M" (evaluate modelB sponsorActivities AiNative (price 20.0) {noStress with ExtraordinaryCost = 1.0e6} s5)
// servicing-only org: Model B without CTO and engineer, non-personnel minus platform lines
let servOnly = { modelB with Name="servicing-only"; Core = modelB.Core |> List.filter (fun r -> not (r.Title.StartsWith "CTO" || r.Title.StartsWith "Senior software")) }
show "R-servonly-ainative" (evaluate servOnly sponsorActivities AiNative (price 20.0) noStress s5)
let s1 = (shapeOf 1 150000.0).Build 1.5e9
show "R1-modelB-ainative" (evaluate modelB sponsorActivities AiNative (price 20.0) noStress s1)
let s10 = (shapeOf 10 150000.0).Build 1.5e9
show "R10-modelB-ainative" (evaluate modelB sponsorActivities AiNative (price 20.0) noStress s10)
let sb = (shapeOf 5 150000.0).Build 3.0e9
show "R3B-modelB-ainative" (evaluate modelB sponsorActivities AiNative (price 20.0) noStress sb)
