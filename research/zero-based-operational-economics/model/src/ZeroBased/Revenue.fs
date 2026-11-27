/// Revenue structures and break-even search over step-function costs. Pure.
module ZeroBased.Revenue

open ZeroBased.Volume

type Pricing =
    | AumBps of bps: float
    | PerAccount of usd: float
    | PerSponsor of usd: float
    | Transaction of perGrant: float * perContribution: float
    | MinimumCommitment of bps: float * minimumPerSponsor: float
    | HybridLicence of basePerSponsor: float * bps: float
    | TieredBps of (float * float) list // (assets up to, bps) per sponsor, marginal tiers
    | ExceptionFees of bps: float * perException: float

let pricingName p =
    match p with
    | AumBps b -> $"AUA fee {b} bps"
    | PerAccount u -> $"Per-account licence ${u}"
    | PerSponsor u -> $"Per-sponsor licence ${u}"
    | Transaction(g, c) -> $"Transaction ${g}/grant + ${c}/contribution"
    | MinimumCommitment(b, m) -> $"{b} bps with ${m} minimum per sponsor"
    | HybridLicence(baseFee, b) -> $"${baseFee}/sponsor base + {b} bps"
    | TieredBps _ -> "Tiered bps (declining marginal)"
    | ExceptionFees(b, e) -> $"{b} bps + ${e} per human exception"

/// Marginal tiered fee on one sponsor's assets.
let tiered (tiers: (float * float) list) (a: float) =
    tiers
    |> List.fold (fun (prev, acc) (upTo, bps) ->
        let slice = max 0.0 (min a upTo - prev)
        upTo, acc + slice * bps / 10000.0) (0.0, 0.0)
    |> snd

/// Annual revenue. Sponsors are assumed equal-sized here; concentration is modelled in Analysis.
let revenue (p: Pricing) (s: Scenario) (c: Counts) (humanExceptions: float) : float =
    let a = assets s
    let perSponsorAssets = if s.Sponsors > 0.0 then a / s.Sponsors else 0.0
    match p with
    | AumBps b -> a * b / 10000.0
    | PerAccount u -> c.Accounts * u
    | PerSponsor u -> s.Sponsors * u
    | Transaction(g, k) -> c.Grants * g + c.Contributions * k
    | MinimumCommitment(b, m) -> s.Sponsors * max m (perSponsorAssets * b / 10000.0)
    | HybridLicence(baseFee, b) -> s.Sponsors * baseFee + a * b / 10000.0
    | TieredBps ts -> s.Sponsors * tiered ts perSponsorAssets
    | ExceptionFees(b, e) -> a * b / 10000.0 + humanExceptions * e

/// Log-spaced account grid used for break-even searches.
let accountGrid (lo: float) (hi: float) (points: int) =
    [ for i in 0 .. points - 1 -> lo * (hi / lo) ** (float i / float (points - 1)) ]

/// Smallest grid value from which profit stays non-negative for every larger grid value.
/// Step costs make profit non-monotonic, so "first crossing" alone would mislead.
let sustainedBreakEven (profit: float -> float) (grid: float list) : float option =
    let ps = grid |> List.map (fun x -> x, profit x)
    let rec go (xs: (float * float) list) (candidate: float option) =
        match xs with
        | [] -> candidate
        | (x, p) :: rest -> if p >= 0.0 then go rest (Option.orElse (Some x) candidate) else go rest None
    go ps None
