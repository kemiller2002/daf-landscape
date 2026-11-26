/// Deterministic pseudo-random sampling (pure: the generator state is threaded explicitly).
module CompetitiveDisplacement.Sampling

open CompetitiveDisplacement.Inputs

/// 64-bit linear congruential generator (Knuth MMIX constants). Returns a uniform in [0,1) and the next state.
let next (state: uint64) : float * uint64 =
    let s = state * 6364136223846793005UL + 1442695040888963407UL
    float (s >>> 11) / float (1UL <<< 53), s

/// Inverse-CDF triangular(low, mode, high) sample from a uniform u.
let triangular (r: Range) (u: float) : float =
    if r.High <= r.Low then r.Base
    else
        let c = (r.Base - r.Low) / (r.High - r.Low)
        if u < c then r.Low + sqrt (u * (r.High - r.Low) * (r.Base - r.Low))
        else r.High - sqrt ((1.0 - u) * (r.High - r.Low) * (r.High - r.Base))

/// Draws one value per parameter name (in sorted-name order, so draws are reproducible).
let drawParams (ps: Params) (state: uint64) : Map<string, float> * uint64 =
    ps
    |> Map.toList
    |> List.fold (fun (acc, st) (name, r) -> let u, st' = next st in Map.add name (triangular r u) acc, st') (Map.empty, state)

/// n independent draws from a seed.
let draws (n: int) (seed: uint64) (ps: Params) : Map<string, float> list =
    List.unfold (fun (i, st) -> if i >= n then None else let d, st' = drawParams ps st in Some(d, (i + 1, st'))) (0, seed)

/// Point values at one level for every parameter.
let atLevel (level: Level) (ps: Params) : Map<string, float> = ps |> Map.map (fun _ r -> pick level r)

/// Empirical percentile (nearest-rank) of a list; infinity is kept as a value ("never").
let percentile (p: float) (xs: float list) : float =
    match List.sort xs with
    | [] -> nan
    | sorted ->
        let n = List.length sorted
        let idx = max 0 (min (n - 1) (int (ceil (p * float n)) - 1))
        List.item idx sorted
