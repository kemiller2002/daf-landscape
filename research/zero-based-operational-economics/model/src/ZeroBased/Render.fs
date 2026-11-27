/// Pure formatting helpers for markdown and CSV outputs.
module ZeroBased.Render

open System.Globalization

let inv = CultureInfo.InvariantCulture

let money (x: float) =
    if System.Double.IsInfinity x || System.Double.IsNaN x then "never"
    elif abs x >= 1e9 then (x / 1e9).ToString("0.00", inv) + "B"
    elif abs x >= 1e6 then (x / 1e6).ToString("0.00", inv) + "M"
    elif abs x >= 1e3 then (x / 1e3).ToString("0.0", inv) + "k"
    else x.ToString("0.00", inv)

let usd x = if System.Double.IsInfinity x || System.Double.IsNaN x then "never" else "$" + money x

let n0 (x: float) = if System.Double.IsNaN x then "n/a" elif System.Double.IsInfinity x then "never" else x.ToString("#,0", inv)
let n1 (x: float) = if System.Double.IsNaN x then "n/a" elif System.Double.IsInfinity x then "never" else x.ToString("#,0.0", inv)
let n2 (x: float) = if System.Double.IsNaN x then "n/a" elif System.Double.IsInfinity x then "never" else x.ToString("#,0.00", inv)
let pct (x: float) = if System.Double.IsNaN x then "n/a" else (x * 100.0).ToString("0.0", inv) + "%"
let f4 (x: float) = if System.Double.IsInfinity x then "Infinity" elif System.Double.IsNaN x then "NaN" else x.ToString("0.####", inv)

let table (header: string list) (rows: string list list) =
    let line cells = "| " + String.concat " | " cells + " |"
    [ line header; line (header |> List.map (fun _ -> "---")) ] @ (rows |> List.map line) |> String.concat "\n"

let csv (header: string list) (rows: string list list) = CompetitiveDisplacement.Csv.write header rows
