/// Deterministic pseudo-random sampling, adapted from the Phase II model (competitive-displacement/model/Sampling.fs).
/// Pure: the generator state is threaded explicitly. Correlation uses Phase II's common-adverse-quantile method,
/// applied per correlation group instead of across all parameters.
module CompetitiveAdvantageCreation.Sampling

open CompetitiveAdvantageCreation.Domain

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

/// One draw of quantiles for named variables. Variables in the same correlation group share, with probability rho,
/// a common quantile oriented so that a high quantile is adverse for every member; otherwise each draws its own.
/// Returns name -> quantile in [0,1) expressed on the variable's own low..high axis.
let drawQuantiles (rho: float) (vars: (string * string * Adverse) list) (state: uint64) : Map<string, float> * uint64 =
    let groups = vars |> List.map (fun (_, g, _) -> g) |> List.distinct |> List.sort
    let commons, st0 =
        groups |> List.fold (fun (acc, st) g -> let u, st' = next st in Map.add g u acc, st') (Map.empty, state)
    vars
    |> List.sortBy (fun (n, _, _) -> n)
    |> List.fold
        (fun (acc, st) (name, group, adv) ->
            let pick, st1 = next st
            let own, st2 = next st1
            let common =
                let u = Map.find group commons
                match adv with
                | HighIsAdverse -> u
                | LowIsAdverse -> 1.0 - u
            let u = if group <> "" && pick < rho then common else own
            Map.add name u acc, st2)
        (Map.empty, st0)

let drawMany (n: int) (seed: uint64) (rho: float) (vars: (string * string * Adverse) list) : Map<string, float> list =
    List.unfold (fun (i, st) -> if i >= n then None else let d, st' = drawQuantiles rho vars st in Some(d, (i + 1, st'))) (0, seed)

/// Empirical percentile (nearest-rank); infinity is kept as a value ("never").
let percentile (p: float) (xs: float list) : float =
    match List.sort xs with
    | [] -> nan
    | sorted ->
        let n = List.length sorted
        let idx = max 0 (min (n - 1) (int (ceil (p * float n)) - 1))
        List.item idx sorted
