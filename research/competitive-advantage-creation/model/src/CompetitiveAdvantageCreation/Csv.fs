/// Minimal RFC 4180 CSV reader and writer (copied from the Phase II model, competitive-displacement/model). Pure.
module CompetitiveAdvantageCreation.Csv

open System
open System.Globalization

type Row = Map<string, string>

/// Splits CSV text into records of fields, honouring quotes, escaped quotes and embedded newlines.
let parseRecords (text: string) : string list list =
    let folder (fields, field: string, inQuotes, prevQuote, records) (c: char) =
        match inQuotes, c with
        | true, '"' when prevQuote -> (fields, field + "\"", true, false, records)
        | true, '"' -> (fields, field, true, true, records)
        | true, _ when prevQuote ->
            // the previous quote closed the quoted section
            match c with
            | ',' -> (field :: fields, "", false, false, records)
            | '\n' -> ([], "", false, false, List.rev (field :: fields) :: records)
            | '\r' -> (fields, field, false, false, records)
            | _ -> (fields, field + string c, false, false, records)
        | true, _ -> (fields, field + string c, true, false, records)
        | false, '"' when field = "" -> (fields, field, true, false, records)
        | false, ',' -> (field :: fields, "", false, false, records)
        | false, '\n' -> ([], "", false, false, List.rev (field :: fields) :: records)
        | false, '\r' -> (fields, field, false, false, records)
        | false, _ -> (fields, field + string c, false, false, records)
    let fields, field, _, _, records = text |> Seq.fold folder ([], "", false, false, [])
    let last = if field = "" && List.isEmpty fields then [] else [ List.rev (field :: fields) ]
    (List.rev records) @ last |> List.filter (fun r -> r <> [ "" ])

/// Header-keyed rows. Returns the header and the rows.
let parse (text: string) : string list * Row list =
    match parseRecords text with
    | [] -> [], []
    | header :: rows ->
        let h = header |> List.map (fun s -> s.Trim())
        h, rows |> List.map (fun r -> List.zip h (r @ List.replicate (max 0 (h.Length - r.Length)) "" |> List.truncate h.Length) |> Map.ofList)

let get (key: string) (row: Row) : Result<string, string> =
    match Map.tryFind key row with
    | Some v -> Ok v
    | None -> Error $"missing column '{key}'"

let num (key: string) (row: Row) : Result<float, string> =
    get key row
    |> Result.bind (fun v ->
        match Double.TryParse(v, NumberStyles.Float, CultureInfo.InvariantCulture) with
        | true, x -> Ok x
        | _ -> Error $"column '{key}' value '{v}' is not a number")

let quote (s: string) =
    if s.IndexOfAny([| ','; '"'; '\n'; '\r' |]) >= 0 then "\"" + s.Replace("\"", "\"\"") + "\"" else s

let fmt (x: float) = x.ToString("0.####", CultureInfo.InvariantCulture)

let write (header: string list) (rows: string list list) : string =
    (header :: rows) |> List.map (List.map quote >> String.concat ",") |> String.concat "\n" |> fun s -> s + "\n"
