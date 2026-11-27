/// Model 3: charity intelligence registry run cost by monitoring mode and the marginal cost per sponsor
/// (agent HI's components, data/fragments/HI/model-registry-components.csv; report 11 section 7). Pure.
module CompetitiveAdvantageCreation.Registry

open CompetitiveAdvantageCreation.Domain

type Scaling =
    | PerRegistry
    | PerConnector
    | PerUnionCharity
    | PerSponsor
    | PerSponsorCharity
    | OwnerFloor
    | Parameter

/// Engineering, labour or sponsor-specific: decides whether the line overlaps a platform's engineering budget
/// (GAP-HI010) and whether it sits under the accountable-owner floor.
type Kind =
    | Engineering
    | Counsel
    | SharedLabour
    /// Human deep review of a charity for a sponsor's reliance (RCH-09, RCH-11). Revision 3: a sponsor control
    /// (RR-REQ-X-007-r1 sponsor policy; reliance written to the sponsor's partition; CNV-GRT-003 reuse only as input),
    /// so it is per sponsor-charity and not shared across sponsors through the union exponent (REV3011, REV4014).
    | DeepReview
    | SponsorSpecific
    | Floor
    | Driver

type Component =
    { Id: string
      Name: string
      Modes: string list
      Cost: Range
      Scaling: Scaling
      Kind: Kind
      AssumptionIds: string list }

type Drivers =
    { CharitiesPerSponsor: float
      Sponsors: float }

type RegistryCost =
    { Mode: string
      Union: float
      Engineering: float
      Counsel: float
      SharedLabour: float
      DeepReview: float
      FloorApplied: float
      SponsorSpecificPerSponsor: float
      Shared: float
      Total: float }

let modes = [ "M1"; "M2"; "M3"; "M4"; "M5" ]

let applies (mode: string) (c: Component) = c.Modes = [ "all" ] || List.contains mode c.Modes

let private value (c: Case) (comps: Component list) (id: string) =
    comps |> List.tryFind (fun x -> x.Id = id) |> Option.map (fun x -> cost c x.Cost) |> Option.defaultValue 0.0

/// Options for the deep-review lines (Revision 3).
type Options =
    { /// Multiplier on deep-review cost: (reviews per charity-year / 2) x (tiered minutes factor). 1.0 = revision 2.
      ReviewFactor: float
      /// Revision 2 shared the deep review across sponsors through the union and counted it under the owner floor.
      DeepReviewShared: bool }

let revision2Options = { ReviewFactor = 1.0; DeepReviewShared = true }

/// connectors: P3-ASM-HI001 (8/10/12), passed as a case value. Modes: M1..M5 (agent HI); "M1T" is M1 with a
/// risk-tiered attested human review (its time saving enters through ReviewFactor).
let runCostWith (o: Options) (c: Case) (connectors: float) (comps: Component list) (mode: string) (d: Drivers) : RegistryCost =
    let mode = if mode = "M1T" then "M1" else mode
    let exponent = value c comps "RCH-18"
    let union = d.CharitiesPerSponsor * (d.Sponsors ** exponent)
    let lineCost (x: Component) =
        let v = cost c x.Cost
        match x.Scaling with
        | PerRegistry -> v
        | PerConnector -> v * connectors
        | PerUnionCharity -> v * union
        | PerSponsor -> v
        | PerSponsorCharity -> v * d.CharitiesPerSponsor
        | OwnerFloor | Parameter -> 0.0
    let deepLine (x: Component) =
        let v = cost c x.Cost * o.ReviewFactor
        if o.DeepReviewShared then v * union else v * d.CharitiesPerSponsor * d.Sponsors
    let active = comps |> List.filter (applies mode)
    let sumKind k = active |> List.filter (fun x -> x.Kind = k) |> List.sumBy lineCost
    let engineering = sumKind Engineering
    let counsel = sumKind Counsel
    let deep = active |> List.filter (fun x -> x.Kind = DeepReview) |> List.sumBy deepLine
    let labour = sumKind SharedLabour
    let floor = value c comps "RCH-05"
    // revision 2 counted the deep review inside the shared labour that the owner floor bounds
    let underFloor = if o.DeepReviewShared then labour + deep else labour
    let floorTopUp = max 0.0 (floor - underFloor)
    let perSponsor = sumKind SponsorSpecific
    let shared = engineering + counsel + labour + floorTopUp + (if o.DeepReviewShared then deep else 0.0)
    let total = shared + (if o.DeepReviewShared then 0.0 else deep) + perSponsor * d.Sponsors
    { Mode = mode; Union = union; Engineering = engineering; Counsel = counsel; SharedLabour = labour; DeepReview = deep
      FloorApplied = floorTopUp; SponsorSpecificPerSponsor = perSponsor; Shared = shared
      Total = total }

let runCost (c: Case) (connectors: float) (comps: Component list) (mode: string) (d: Drivers) : RegistryCost =
    runCostWith revision2Options c connectors comps mode d

/// Cost of adding one more sponsor with the same number of charities in use.
let marginalSponsor (c: Case) (connectors: float) (comps: Component list) (mode: string) (d: Drivers) =
    (runCostWith { ReviewFactor = 1.0; DeepReviewShared = false } c connectors comps mode { d with Sponsors = d.Sponsors + 1.0 }).Total
    - (runCostWith { ReviewFactor = 1.0; DeepReviewShared = false } c connectors comps mode d).Total

/// GAP-HI010 rule (traced in report 18). Phase II enterprise modes MD-3..MD-7 carry a platform engineering team and
/// charity-data subscriptions in fixed cost (PR #87 layer B, built into MD fixed cost), and price vetting labour in
/// event EV-E08 minutes; adding any registry line to them double counts (report 10 section 9 items 1 and 9), so
/// nothing is addable. The Phase III lean licensor run (agent AB) carries no registry at all, so the shared layer and
/// the vendor-run labour are added, except the share of engineering and counsel that the lean maintenance and
/// corporate-admin budgets are assumed to absorb. Sponsor-specific decisions stay with the sponsor (segregated) and
/// are not a vendor cost in licensing.
type Target =
    | PhaseTwoMode
    | LeanLicensor of engineeringAndCounselAbsorbed: float

/// Who performs the human deep review under licensing (Revision 3, proposed owner decision P3-DEC-MOD005).
type Performer =
    | Vendor
    | Sponsor

/// Vendor-borne registry cost: shared labour, the owner-floor top-up, the unabsorbed share of engineering and counsel,
/// and the deep review only when the vendor performs it. Sponsor-specific decisions stay with the sponsor.
let addableBy (performer: Performer) (target: Target) (r: RegistryCost) =
    match target with
    | PhaseTwoMode -> 0.0
    | LeanLicensor absorbed ->
        r.SharedLabour + r.FloorApplied + (r.Engineering + r.Counsel) * (1.0 - max 0.0 (min 1.0 absorbed))
        + (match performer with Vendor -> r.DeepReview | Sponsor -> 0.0)

/// Deep-review labour that the sponsor performs (transferred work).
let transferredBy (performer: Performer) (r: RegistryCost) = match performer with Sponsor -> r.DeepReview | Vendor -> 0.0

let addable (target: Target) (r: RegistryCost) = addableBy Vendor target r
