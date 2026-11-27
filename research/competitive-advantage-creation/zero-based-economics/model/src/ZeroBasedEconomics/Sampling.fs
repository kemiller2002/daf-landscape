/// Deterministic sampling (adapted from the Phase II model): LCG, triangular inverse CDF, grouped correlation. Pure.
module ZeroBasedEconomics.Sampling

open ZeroBasedEconomics.Domain

let next (state: uint64) : float * uint64 =
    let s = state * 6364136223846793005UL + 1442695040888963407UL
    float (s >>> 11) / float (1UL <<< 53), s

let triangular (r: Range) (u: float) : float =
    if r.High <= r.Low then r.Base
    else
        let c = (r.Base - r.Low) / (r.High - r.Low)
        if u < c then r.Low + sqrt (u * (r.High - r.Low) * (r.Base - r.Low))
        else r.High - sqrt ((1.0 - u) * (r.High - r.Low) * (r.High - r.Base))

/// One draw: a quantile per named range. With probability rho a range takes the draw's common adverse quantile
/// (high = adverse unless the name is in `lowIsAdverse`), otherwise its own.
let drawQuantiles (rho: float) (lowIsAdverse: string -> bool) (names: string list) (state: uint64) : Map<string, float> * uint64 =
    let uCommon, st0 = next state
    names
    |> List.fold (fun (acc, st) name ->
        let pickU, st1 = next st
        let own, st2 = next st1
        let common = if lowIsAdverse name then 1.0 - uCommon else uCommon
        Map.add name (if pickU < rho then common else own) acc, st2) (Map.empty, st0)

let quantileDraws (n: int) (seed: uint64) (rho: float) (lowIsAdverse: string -> bool) (names: string list) =
    List.unfold (fun (i, st) -> if i >= n then None else let d, st' = drawQuantiles rho lowIsAdverse names st in Some(d, (i + 1, st'))) (0, seed)

/// Nearest-rank percentile; empty input gives NaN.
let percentile (p: float) (xs: float list) : float =
    match List.sort xs with
    | [] -> nan
    | sorted ->
        let n = List.length sorted
        List.item (max 0 (min (n - 1) (int (ceil (p * float n)) - 1))) sorted
