/// Formatting helpers for Markdown tables and CSV. Pure functions.
module ServicingEconomics.Render

open System
open System.Globalization

let inv = CultureInfo.InvariantCulture

let usd (v: float) =
    if Double.IsNaN v then "n/a"
    elif abs v >= 1.0e9 then (v / 1.0e9).ToString("0.00", inv) + "B"
    elif abs v >= 1.0e6 then (v / 1.0e6).ToString("0.00", inv) + "M"
    elif abs v >= 1.0e3 then (v / 1.0e3).ToString("0", inv) + "k"
    else v.ToString("0", inv)

let money (v: float) = if Double.IsNaN v then "n/a" else "$" + usd v

let pct (v: float) = if Double.IsNaN v || Double.IsInfinity v then "n/a" else (v * 100.0).ToString("0.0", inv) + "%"

let num (digits: int) (v: float) = if Double.IsNaN v then "n/a" else v.ToString("F" + string digits, inv)

let optMoney = function Some v -> money v | None -> "not reached ≤ $20B"

let table (headers: string list) (rows: string list list) =
    let line (cells: string list) = "| " + String.concat " | " cells + " |"
    String.concat "\n" ([ line headers; "|" + String.concat "|" (headers |> List.map (fun _ -> "---")) + "|" ] @ (rows |> List.map line))

let csvCell (s: string) = if s.Contains "," || s.Contains "\"" then "\"" + s.Replace("\"", "\"\"") + "\"" else s

let csv (headers: string list) (rows: string list list) =
    String.concat "\n" ((headers :: rows) |> List.map (fun r -> String.concat "," (r |> List.map csvCell))) + "\n"
