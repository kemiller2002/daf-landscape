/// Event-level cost model: every operational event is priced per operating mode from explicit rules.
module CompetitiveDisplacement.Events

open CompetitiveDisplacement.Inputs

type Values = Map<string, float>

let v (vals: Values) key = Map.find key vals

let rate (vals: Values) (expertise: string) = v vals ("rate_" + expertise)

/// Cost of one event for one account-year (or per sponsor-year for sponsor-level work).
type EventCost =
    { EventId: string
      Name: string
      Frequency: float
      TouchProb: float
      MinutesPerTouch: float
      HumanMinutesPerAcct: float
      LabourPerAcct: float
      VendorExternalPerAcct: float
      PassThroughPerAcct: float
      AiPerAcct: float
      PreventionPerAcct: float
      ExpectedFailurePerAcct: float
      SuccessCostPerEvent: float
      FailureLifecycleCost: float
      SponsorLevelMinutes: float
      SponsorLevelCost: float
      OnetimeCost: float
      OnetimePerAcctCost: float }

let private prevented (mode: Mode) (vals: Values) (e: EventDef) =
    if mode.UsesPrevention then e.PrevEfficacy * v vals "prevention_scale" else 0.0

/// Touch probability under a mode's touch rule.
let touchProb (mode: Mode) (vals: Values) (e: EventDef) : float =
    let native = min 1.0 (e.PNative * v vals "touch_mult_native")
    let raw =
        match mode.TouchRule with
        | "conv" -> e.PConv
        | "structured_native" -> if e.Structured then native else e.PConv
        | _ -> native
    raw * (1.0 - prevented mode vals e)

/// Minutes per touch. "Exception without AI" scales native minutes back up by the AI assistance factor,
/// so the difference between exception-driven and AI-native modes is the AI effect alone.
let minutesPerTouch (mode: Mode) (vals: Values) (e: EventDef) : float =
    let f = v vals "ai_assist_duration_factor"
    let nativeD = e.DNative * v vals "duration_mult_native"
    let exceptionNoAi = nativeD / f
    match mode.DurationRule, mode.TouchRule with
    | "conv", "structured_native" -> if e.Structured then exceptionNoAi else e.DConv
    | "conv", "native" -> exceptionNoAi
    | "conv", _ -> e.DConv
    | "ai_assist", _ -> e.DConv * f
    | _, _ -> nativeD

let private sponsorFactor (rule: string) (vals: Values) (conv: float) (native: float) =
    match rule with
    | "conv" -> conv
    | "ai_assist" -> conv * v vals "sponsor_min_factor_ai_assist"
    | "midpoint" -> (conv + native) / 2.0
    | _ -> native

let failMult (mode: Mode) (vals: Values) =
    if mode.FailRule = "conventional" then v vals "fail_mult_conventional" else v vals "fail_mult_automated"

let cost (mode: Mode) (vals: Values) (e: EventDef) : EventCost =
    let r = rate vals e.Expertise
    let freq = e.Freq.Base * v vals "activity_mult"
    let p = touchProb mode vals e
    let d = minutesPerTouch mode vals e
    let minutes = freq * p * d
    let aiScale = if mode.UsesAi then v vals "ai_routine_scale" else 0.0
    let aiPerEvent = aiScale * (e.AiCostRoutine + p * e.AiCostTouch)
    let prevCost = if mode.UsesPrevention && e.PrevEfficacy > 0.0 then e.PrevCost else 0.0
    let failP = e.FailProb * failMult mode vals * (1.0 - prevented mode vals e)
    let failCost = e.FailMinutes / 60.0 * r + e.FailExternal + e.FailLoss
    let ext = if e.PassThrough then 0.0 else e.External
    let pass = if e.PassThrough then e.External else 0.0
    let successCost = p * d / 60.0 * r + e.External + aiPerEvent + prevCost
    let sponsorMin = sponsorFactor mode.SponsorRule vals e.SponsorMinConv e.SponsorMinNative
    let onetimeMin = sponsorFactor mode.SponsorRule vals e.OnetimeMinConv e.OnetimeMinNative
    let onetimePerAcct = sponsorFactor mode.SponsorRule vals e.OnetimePerAcctConv e.OnetimePerAcctNative
    { EventId = e.Id
      Name = e.Name
      Frequency = freq
      TouchProb = p
      MinutesPerTouch = d
      HumanMinutesPerAcct = minutes
      LabourPerAcct = minutes / 60.0 * r
      VendorExternalPerAcct = freq * ext
      PassThroughPerAcct = freq * pass
      AiPerAcct = freq * aiPerEvent
      PreventionPerAcct = freq * prevCost
      ExpectedFailurePerAcct = freq * failP * failCost
      SuccessCostPerEvent = successCost
      FailureLifecycleCost = successCost + failCost
      SponsorLevelMinutes = sponsorMin
      SponsorLevelCost = sponsorMin / 60.0 * r
      OnetimeCost = onetimeMin / 60.0 * r
      OnetimePerAcctCost = onetimePerAcct / 60.0 * r }

/// Total per-account cost of an event excluding sponsor pass-through rails.
let perAccount (c: EventCost) =
    c.LabourPerAcct + c.VendorExternalPerAcct + c.AiPerAcct + c.PreventionPerAcct + c.ExpectedFailurePerAcct

let costs (mode: Mode) (vals: Values) (events: EventDef list) = events |> List.map (cost mode vals)
