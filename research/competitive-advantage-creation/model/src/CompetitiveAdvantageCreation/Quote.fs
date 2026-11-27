/// Quoting model output tables into reports. A report marks a block with
/// `<!-- model-output: tables/NAME.md -->` ... `<!-- /model-output -->`; `quote` replaces the block body with the
/// generated table and `validate` fails when a block differs, so report numbers are never hand-typed. Pure.
module CompetitiveAdvantageCreation.Quote

open System.Text.RegularExpressions

let private pattern = Regex(@"<!-- model-output: (?<name>[^ ]+) -->\n(?<body>.*?)<!-- /model-output -->", RegexOptions.Singleline)

/// Names of the tables a document quotes.
let quoted (text: string) = pattern.Matches(text) |> Seq.map (fun m -> m.Groups.["name"].Value) |> List.ofSeq

/// Replace every block body with the current table. Unknown names are left unchanged and reported.
let fill (lookup: string -> string option) (text: string) : string * string list =
    let missing = quoted text |> List.filter (fun n -> (lookup n).IsNone)
    let filled =
        pattern.Replace(text, MatchEvaluator(fun m ->
            let name = m.Groups.["name"].Value
            match lookup name with
            | Some t -> $"<!-- model-output: {name} -->\n{t}<!-- /model-output -->"
            | None -> m.Value))
    filled, missing

/// Errors for blocks whose body differs from the current table or whose table does not exist.
let check (docName: string) (lookup: string -> string option) (text: string) : string list =
    pattern.Matches(text)
    |> Seq.choose (fun m ->
        let name = m.Groups.["name"].Value
        match lookup name with
        | None -> Some $"{docName}: quotes unknown model output {name}"
        | Some t when t <> m.Groups.["body"].Value -> Some $"{docName}: quoted block {name} differs from the model output (run `quote`)"
        | Some _ -> None)
    |> List.ofSeq
