/// Pure, seeded simulation primitives shared by the workflow-innovation experiments.
/// No global state: every draw returns the value and the next generator.
module Daf.Experiments.Sim

open System

/// SplitMix64 generator state.
type Rng = Rng of uint64

let private mix (z: uint64) =
    let z = (z ^^^ (z >>> 30)) * 0xbf58476d1ce4e5b9UL
    let z = (z ^^^ (z >>> 27)) * 0x94d049bb133111ebUL
    z ^^^ (z >>> 31)

let next (Rng s) =
    let s' = s + 0x9e3779b97f4a7c15UL
    mix s', Rng s'

/// Uniform in [0, 1).
let uniform rng =
    let (v, r) = next rng
    float (v >>> 11) / float (1UL <<< 53), r

let bernoulli p rng =
    let (u, r) = uniform rng
    u < p, r

/// Unfold n draws from a generator function.
let draws n (f: Rng -> 'a * Rng) rng =
    let rec go k acc r =
        if k = 0 then List.rev acc, r
        else
            let (x, r') = f r
            go (k - 1) (x :: acc) r'
    go n [] rng

/// Zipf-like recipient popularity: weight(i) = 1 / (i + 1)^s, normalised; sampled by inverse CDF.
type Zipf = { Cdf: float[] }

let zipf (n: int) (s: float) =
    let w = Array.init n (fun i -> 1.0 / Math.Pow(float (i + 1), s))
    let total = Array.sum w
    { Cdf = w |> Array.scan (+) 0.0 |> Array.tail |> Array.map (fun c -> c / total) }

let sampleZipf (z: Zipf) rng =
    let (u, r) = uniform rng
    let idx = Array.BinarySearch(z.Cdf, u)
    (if idx >= 0 then idx else min (z.Cdf.Length - 1) (~~~idx)), r

/// Share of draws captured by the top k ranks (for calibration against observed concentration).
let topShare (z: Zipf) k = if k <= 0 then 0.0 else z.Cdf.[min (k - 1) (z.Cdf.Length - 1)]

/// Gini coefficient of a non-negative sample.
let gini (xs: float list) =
    let a = xs |> List.sort |> Array.ofList
    let n = float a.Length
    if n = 0.0 || Array.sum a = 0.0 then 0.0
    else
        let weighted = a |> Array.mapi (fun i x -> float (i + 1) * x) |> Array.sum
        (2.0 * weighted) / (n * Array.sum a) - (n + 1.0) / n

/// Percentile of a list (nearest-rank).
let percentile p (xs: float list) =
    match List.sort xs with
    | [] -> 0.0
    | s -> s.[max 0 (min (s.Length - 1) (int (ceil (p * float s.Length)) - 1))]
