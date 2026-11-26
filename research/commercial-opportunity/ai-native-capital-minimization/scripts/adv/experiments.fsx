// ADV2 experiments against the copied, unmodified capital-minimization model (Release DLLs).
#r "/tmp/claude-0/-home-user/45711cf3-dc26-5c8e-a6da-4af8bd5f0946/scratchpad/aincm/adv/work/aincm-copy/model/src/CapitalMinimization/bin/Release/net10.0/ServicingEconomics.dll"
#r "/tmp/claude-0/-home-user/45711cf3-dc26-5c8e-a6da-4af8bd5f0946/scratchpad/aincm/adv/work/aincm-copy/model/src/CapitalMinimization/bin/Release/net10.0/CapitalMinimization.dll"
open ServicingEconomics.Domain
open ServicingEconomics.Economics
open ServicingEconomics.Parameters
open ServicingEconomics.Analysis
open CapitalMinimization.Design
open CapitalMinimization.Layers
open CapitalMinimization.Development
open CapitalMinimization.Designs
open CapitalMinimization.Sequences

let shape n b = equalSponsors n (sponsor "sponsor" 1000.0 b)
let m (v: float) = sprintf "$%.2fM" (v / 1e6)
let ob = function Some (v: float) -> sprintf "$%.2fB" (v / 1e9) | None -> "not reached"
let be d t st = snd (assetsForMarginDesign d t (price 20.0) st (shape 5 250000.0) 0.0)
let charge amount = { noStress with Name = "layer charge"; ExtraordinaryCost = amount }
let standaloneCharge lc d = servicingCost Standalone lc (fun x -> fixedCost x) d - fixedCost d
let beStand lc d t = be d t (charge (standaloneCharge lc d))
let p fmt = Printf.printfn fmt

p "== E01 control-feasible headline (50 min, standalone baseLayers)"
for d in designs do
  let r = evaluateDesign d 50.0 (price 20.0) noStress ((shape 5 250000.0).Build 1.0e9)
  p "%s | feasible=%b | operating BE %s | standalone BE %s" d.Name r.ControlFeasible (ob (be d 50.0 noStress)) (ob (beStand baseLayers d 50.0))

p "== E02 coordination double count: set CoordinationHoursPerPairWeek=0"
for d in [f3; f5; f8] do
  let d0 = { d with CoordinationHoursPerPairWeek = 0.0 }
  let r = evaluateDesign d 50.0 (price 20.0) noStress ((shape 5 250000.0).Build 1.5e9)
  p "%s coord cost at $1.5B %s | BE %s -> %s" d.Name (m r.CoordinationCost) (ob (be d 50.0 noStress)) (ob (be d0 50.0 noStress))

p "== E03 outcome-designed +3%% productive hours: effect isolated (30.1 min, sponsor 12,720)"
for d in [f3; f5] do
  let od = outcomeDesigned d
  let odNo = { od with ProductiveHours = d.ProductiveHours }
  for a in [1.0e9; 2.5e9; 5.0e9] do
    let ss = (shape 5 250000.0).Build a
    let c1 = (evaluateDesign od outcomeDesignedTarget (price 20.0) noStress ss).Base.TotalCost
    let c0 = (evaluateDesign odNo outcomeDesignedTarget (price 20.0) noStress ss).Base.TotalCost
    p "%s at %s: with +3%% %s, without %s, diff %s" d.Name (m a) (m c1) (m c0) (m (c1 - c0))

p "== E04 December sets headcount: December excess covered by employees instead of +50%% premium hours"
// Cost of covering the December excess E (hours) with full-year employees: E / (q/12) FTE x loaded cost (= 1520 h x rate).
let decHeadcountCost (d: Design) t a frac =
  let r = evaluateDesign d t (price 20.0) noStress ((shape 5 250000.0).Build a)
  let q = d.ProductiveHours * d.Utilisation
  let extra =
    r.Pools |> List.sumBy (fun pr ->
      let pool = d.Pools |> List.find (fun x -> x.Name = pr.Pool)
      let rate = pool.LoadedHourly
      let excessHours = pr.PeakCost / (rate * (1.0 + d.PeakPremium))
      let fte = excessHours / (q / 12.0)
      frac * (fte * d.ProductiveHours * rate - pr.PeakCost))
  r, extra
for d in [f3; f5] do
  for a in [1.0e9; 1.5e9; 2.5e9; 5.0e9] do
    let r, extra = decHeadcountCost d 50.0 a 1.0
    let _, half = decHeadcountCost d 50.0 a 0.5
    p "%s at %s (%.0f accts): headcount %.1f + contracted %.1f, peak cost %s; employ-for-December adds %s (all) / %s (half); margin %.1f%% -> %.1f%%" d.Name (m a) r.Base.Accounts r.Headcount r.ContractedFte (m r.Base.PeakCost) (m extra) (m half) (100.0 * r.Base.OperatingMargin) (100.0 * (r.Base.Revenue - r.Base.TotalCost - extra) / r.Base.Revenue)
  // break-even with half of December excess on employees, via fixed-charge approximation evaluated at the margin search
  let beDec frac =
    let eval ss =
      let r = evaluateDesign d 50.0 (price 20.0) noStress ss
      let a = r.Base.AverageAssets
      let _, extra = decHeadcountCost d 50.0 a frac
      { r.Base with TotalCost = r.Base.TotalCost + extra; OperatingProfit = r.Base.OperatingProfit - extra; OperatingMargin = (r.Base.OperatingProfit - extra) / r.Base.Revenue }
    snd (assetsForMargin eval (shape 5 250000.0) 0.0)
  p "%s operating BE: model %s | half Dec excess employed %s | all employed %s" d.Name (ob (be d 50.0 noStress)) (ob (beDec 0.5)) (ob (beDec 1.0))

p "== E05 F3 at break-even scale: employees vs contracted FTE"
for a in [1.0e9; 1.45e9; 2.0e9; 3.0e9] do
  let r = evaluateDesign f3 50.0 (price 20.0) noStress ((shape 5 250000.0).Build a)
  p "F3 %s: employees %.1f contracted FTE %.1f accounts %.0f" (m a) r.Headcount r.ContractedFte r.Base.Accounts

p "== E06 sequences: add omitted recurring platform costs (Echelon share, non-prod, servicing-specific, maintenance gap)"
let embeddedAt (s: Sequence) mo = embeddedEngineering (designAt s mo)
let addPlatform (lc: LayerCosts) (s: Sequence) =
  let rec_ = [ for mo in 0 .. s.Months - 1 ->
                 let firstLive = s.Customers |> List.map (fun c -> c.SignMonth + c.OnboardingMonths) |> List.min
                 let liveNow = mo >= firstLive
                 let gap = if liveNow then max 0.0 (lc.UnboundMaintenance - embeddedAt s mo) else 0.0
                 mo, "omitted platform recurring", (echelonToUnbound lc + lc.UnboundPlatformOps + (if liveNow then lc.ServicingSpecificPlatform else 0.0) + gap) / 12.0 ]
  // Recurring applies from start month onward and sums; use one-time per month instead to vary by month
  { s with Name = s.Name + " | +platform recurring"; OneTime = s.OneTime @ rec_ }
let zeroFin (s: Sequence) = { s with FinancingRate = 0.0 }
let fullBuild1x (s: Sequence) =
  let k = minimumProductCost unboundBaseline 1.0 / minimumBuild
  { s with OneTime = s.OneTime |> List.map (fun (mo, n: string, v) -> if n.Contains "minimum product build" then mo, n, v * k else mo, n, v) }
for s in sequences do
  let c0 = capitalRequired (simulate s)
  let c1 = capitalRequired (simulate (addPlatform baseLayers s))
  let c2 = capitalRequired (simulate (addPlatform lyrLayers s))
  let c3 = capitalRequired (simulate (zeroFin s))
  let c4 = capitalRequired (simulate (fullBuild1x s))
  let c5 = capitalRequired (simulate (economic (addPlatform baseLayers s)))
  let r0 = roic (simulate s)
  let r1 = roic (simulate (addPlatform baseLayers s))
  let fy1 = finalYearProfit (simulate (addPlatform baseLayers s))
  p "%s | base %s | +platform(base) %s | +platform(LYR) %s | no financing %s | MSP at 1x %s | econ+platform %s | ROIC %A -> %A | Y5 profit with platform %s" (s.Name.Split(':').[0]) (m c0) (m c1) (m c2) (m c3) (m c4) (m c5) r0 r1 (m fy1)

p "== E07 minimum build at 1x/1.5x/3x"
for mult in [1.0; 1.5; 2.0; 3.0] do p "MSP at %.1fx: %s" mult (m (minimumProductCost unboundBaseline mult))

p "== E08 scenario matrix sensitivity: combined (50%% share) vs 100%% share; outcome-designed on standalone LYR"
let echelonSupported = { baseLayers with UnboundBuild = minimumProductCost unboundBaseline 3.0 }
let fa lc d t = be (servicingOnly d) t (charge (servicingCost FullyAllocated lc (fun x -> fixedCost x) d - fixedCost (servicingOnly d)))
p "F5 FA 3x share 1.0: %s; share 0.5: %s" (ob (fa echelonSupported f5 50.0)) (ob (fa { echelonSupported with ServicingShareOfUnbound = 0.5 } f5 50.0))
p "Outcome F5 FA 3x: %s; outcome F5 standalone LYR: %s; F5 standalone LYR: %s" (ob (fa echelonSupported (outcomeDesigned f5) outcomeDesignedTarget)) (ob (beStand lyrLayers (outcomeDesigned f5) outcomeDesignedTarget)) (ob (beStand lyrLayers f5 50.0))
p "F5 standalone base layers at 1x build: %s; at 1.5x: %s; at 2x: %s" (ob (beStand { baseLayers with UnboundBuild = minimumProductCost unboundBaseline 1.0 } f5 50.0)) (ob (beStand { baseLayers with UnboundBuild = minimumProductCost unboundBaseline 1.5 } f5 50.0)) (ob (beStand baseLayers f5 50.0))
// LYR base Echelon (0.30M caused + 40% usage) on base layers
let lyrEchelon = { baseLayers with EchelonAnnual = 300000.0; EchelonShareToUnbound = 0.9 }
p "F5 standalone base layers but LYR Echelon reliance: %s" (ob (beStand lyrEchelon f5 50.0))
let sales = { noStress with ExtraordinaryCost = 188000.0 }
p "F5 standalone base + sales restored to $250k (+$188k): %s" (ob (be f5 50.0 { sales with ExtraordinaryCost = 188000.0 + standaloneCharge baseLayers f5 }))

p "== E09 servicingOnly keeps code reviewers (double count with Layer B engineers)"
for d in [f3; f5] do
  let so = servicingOnly d
  p "%s servicingOnly contracted: %A" d.Name (so.Contracted |> List.map fst)

p "== E10 layer charge fixed vs scale: F5 standalone charge at $0.5B, $1B, $3B"
for a in [0.5e9; 1.0e9; 3.0e9] do
  let ss = (shape 5 250000.0).Build a
  let total (x: Design) = (evaluateDesign x 50.0 (price 20.0) noStress ss).Base.TotalCost
  p "%s: standalone charge %s; FA charge %s" (m a) (m (servicingCost Standalone baseLayers total f5 - total f5)) (m (servicingCost FullyAllocated baseLayers total f5 - total (servicingOnly f5)))

p "== E11 per-hire cost with ProductiveHours scaled (addedCost uses ProductiveHours x hourly)"
let od5 = outcomeDesigned f5
p "employee ops cost implied: base %.0f, outcome-designed %.0f (loaded %.0f)" (f5.ProductiveHours * opsLoaded / hours) (od5.ProductiveHours * opsLoaded / hours) opsLoaded

p "== E12 early target only after first go-live (pre-delegation per sponsor ignored)"
for s in [seqB; seqF] do
  let perSponsor = { s with RedesignLagMonths = 24 }
  p "%s capital %s -> lag 24 months %s; Y5 profit %s -> %s" (s.Name.Split(':').[0]) (m (capitalRequired (simulate s))) (m (capitalRequired (simulate perSponsor))) (m (finalYearProfit (simulate s))) (m (finalYearProfit (simulate perSponsor)))

p "== E13 seqF composition: F1 until month 18"
let rowsF = simulate seqF
for mo in [0; 11; 17; 18; 23; 29; 35; 59] do
  let r = rowsF |> List.find (fun r -> r.Month = mo)
  p "m%d live=%d out=%s in=%s cum=%s heads=%.1f" mo r.Live (m r.CashOut) (m r.CashIn) (m r.Cumulative) r.Headcount

p "== E14 combined adjusted break-even (F5 / F3, 50 min, 20 bps, 5 x $250k)"
let combined (d: Design) (lc: LayerCosts) extraFixed decFrac bal bps =
  let c = servicingCost Standalone lc (fun x -> fixedCost x) d - fixedCost d
  let eval ss =
    let r = evaluateDesign d 50.0 (price bps) (charge (c + extraFixed)) ss
    let _, dec = decHeadcountCost d 50.0 r.Base.AverageAssets decFrac
    let prof = r.Base.OperatingProfit - dec
    { r.Base with TotalCost = r.Base.TotalCost + dec; OperatingProfit = prof; OperatingMargin = prof / r.Base.Revenue }
  snd (assetsForMargin eval (shape 5 bal) 0.0)
let lc15 = { baseLayers with UnboundBuild = minimumProductCost unboundBaseline 1.5; EchelonAnnual = 300000.0; EchelonShareToUnbound = 0.9 }
// extra fixed: sales to $250k (+188k), recon/independent reviewer for F5 (+40k), turnover/recruiting (+40k), onboarding churn amortisation (+52k)
for d in [f3; f5] do
  p "%s: model standalone %s | +sales,+reviewer,+turnover,+churn onboarding %s | +Echelon LYR & MSP 1.5x %s | +half Dec employed %s | all of it with LYR platform team %s"
    d.Name (ob (beStand baseLayers d 50.0)) (ob (combined d baseLayers 320000.0 0.0 250000.0 20.0)) (ob (combined d lc15 320000.0 0.0 250000.0 20.0)) (ob (combined d lc15 320000.0 0.5 250000.0 20.0)) (ob (combined d lyrLayers 320000.0 0.5 250000.0 20.0))
p "F5 adjusted (lc15, +320k, half Dec) at $500k balance: %s; at $100k: %s; at 15 bps $250k: %s" (ob (combined f5 lc15 320000.0 0.5 500000.0 20.0)) (ob (combined f5 lc15 320000.0 0.5 100000.0 20.0)) (ob (combined f5 lc15 320000.0 0.5 250000.0 15.0))
let odF5 = outcomeDesigned f5
let cOd = servicingCost Standalone lc15 (fun x -> fixedCost x) odF5 - fixedCost odF5
p "Outcome-designed F5 standalone lc15 +320k: %s" (ob (snd (assetsForMarginDesign odF5 outcomeDesignedTarget (price 20.0) (charge (cOd + 320000.0)) (shape 5 250000.0) 0.0)))

p "== E15 joint failures (modifiers are only applied one at a time in the model)"
for s in [seqB; seqC; seqF; seqG] do
  let j1 = productivityHalved (acquisitionTwiceAsLong s)
  let j2 = humanReviewNotReduced (assuranceHigher (productivityHalved s))
  let r0, r1, r2 = simulate s, simulate j1, simulate j2
  p "%s base %s | build x2 + sales 2x %s (profit month %A) | build x2 + assurance + handling AI-enhanced %s (profit month %A)" (s.Name.Split(':').[0]) (m (capitalRequired r0)) (m (capitalRequired r1)) (monthsToProfit r1) (m (capitalRequired r2)) (monthsToProfit r2)
