/// Charity-vetting prototypes on PUBLIC data (charity-vetting-ai deep dive).
///   V1 recipient resolution: free-text name + address -> EIN, benchmarked against the EIN the sponsor filed on Schedule I.
///   V2 sanctions name screening: alert volume of fuzzy screening of recipient names against OFAC lists.
/// Pure functions over immutable data; file loading is isolated at the bottom.
module Daf.Experiments.Vetting

open System
open System.IO
open System.Text

// ---------------------------------------------------------------- normalisation
let private stop =
    set [ "THE"; "OF"; "AND"; "INC"; "INCORPORATED"; "CORP"; "CORPORATION"; "CO"; "LLC"; "LTD"; "A"; "AN"; "FOR"; "IN"; "AT"; "TO"; "ON"
          "ASSOCIATION"; "ASSN"; "ORGANIZATION"; "ORG"; "FOUNDATION"; "FDN"; "FUND"; "TRUST"; "SOCIETY"; "INTERNATIONAL"; "INTL"
          "AMERICA"; "AMERICAN"; "USA"; "US"; "NATIONAL"; "COMMUNITY"; "CENTER"; "CENTRE"; "CHURCH"; "SCHOOL"; "INSTITUTE"; "COUNCIL" ]

let private synonyms = Map.ofList [ "ST", "SAINT"; "MT", "MOUNT"; "UNIV", "UNIVERSITY"; "CTR", "CENTER"; "&", "AND"; "INTL", "INTERNATIONAL"; "ASSOC", "ASSOCIATION" ]

/// Upper-case, strip punctuation, map synonyms. Keeps all tokens (stop words included) for exact keys.
let tokens (s: string) =
    let cleaned =
        (if isNull s then "" else s.ToUpperInvariant().Replace("'", "").Replace("\u2019", ""))
        |> String.map (fun c -> if Char.IsLetterOrDigit c || c = '&' then c else ' ')
    cleaned.Split([| ' ' |], StringSplitOptions.RemoveEmptyEntries)
    |> Array.map (fun t -> synonyms.TryFind t |> Option.defaultValue t)
    |> List.ofArray

let exactKey (s: string) = tokens s |> List.filter (fun t -> t <> "THE") |> String.concat " "

/// Distinguishing tokens (stop words removed) used for candidate generation and similarity.
let keyTokens (s: string) = tokens s |> List.filter (fun t -> not (stop.Contains t)) |> List.distinct

// ---------------------------------------------------------------- BMF index
type Org =
    { Ein: string
      Name: string
      City: string
      State: string
      Zip5: string
      Subsection: string
      Foundation: string }

type BmfIndex =
    { ByEin: Map<string, Org>
      ByExact: Map<string, Org list>
      ByExactState: Map<string * string, Org list>
      ByTokenState: Map<string * string, Org list>   // (state, distinguishing token) -> orgs
      TokenDf: Map<string, int>
      N: int }

let buildIndex (orgs: Org list) =
    let byEin = orgs |> List.map (fun o -> o.Ein, o) |> Map.ofList
    let group f = orgs |> List.groupBy f |> Map.ofList
    let withTokens = orgs |> List.map (fun o -> o, keyTokens o.Name)
    let df =
        withTokens |> List.collect snd |> List.countBy id |> Map.ofList
    let byTokenState =
        withTokens
        |> List.collect (fun (o, ts) -> ts |> List.map (fun t -> (o.State, t), o))
        |> List.groupBy fst
        |> List.map (fun (k, v) -> k, v |> List.map snd)
        |> Map.ofList
    { ByEin = byEin
      ByExact = group (fun o -> exactKey o.Name)
      ByExactState = group (fun o -> exactKey o.Name, o.State)
      ByTokenState = byTokenState
      TokenDf = df
      N = orgs.Length }

// ---------------------------------------------------------------- V1 resolution
type Query = { Name: string; City: string; State: string; Zip5: string; FiledEin: string }

type Outcome =
    | Resolved of ein: string
    | Ambiguous of candidates: string list   // referred to a person (or an AI adjudicator)
    | NoMatch

type Method =
    | ExactNameNational
    | ExactNameState
    | ExactNameStateCityZip
    | FuzzyTfIdf of threshold: float * margin: float
    | Cascade                 // exact+state+tie-break, then conservative fuzzy (0.95/0.20); otherwise refer with candidates

let private idf (ix: BmfIndex) t =
    let d = ix.TokenDf.TryFind t |> Option.defaultValue 1
    Math.Log(float ix.N / float d)

/// IDF-weighted cosine between distinguishing-token sets, plus small location bonuses.
let similarity (ix: BmfIndex) (q: Query) (o: Org) =
    let qa = keyTokens q.Name |> Set.ofList
    let ob = keyTokens o.Name |> Set.ofList
    let w ts = ts |> Seq.sumBy (fun t -> let v = idf ix t in v * v) |> sqrt
    let inter = Set.intersect qa ob |> Seq.sumBy (fun t -> let v = idf ix t in v * v)
    let denom = w qa * w ob
    let cos = if denom = 0.0 then 0.0 else inter / denom
    let cityBonus = if q.City <> "" && String.Equals(q.City, o.City, StringComparison.OrdinalIgnoreCase) then 0.05 else 0.0
    let zipBonus = if q.Zip5 <> "" && q.Zip5 = o.Zip5 then 0.05 else 0.0
    min 1.0 (cos + cityBonus + zipBonus)

/// Candidate generation: orgs in the same state sharing the query's rarest distinguishing tokens.
let candidates (ix: BmfIndex) (q: Query) (k: int) =
    let rare =
        keyTokens q.Name
        |> List.sortBy (fun t -> ix.TokenDf.TryFind t |> Option.defaultValue 0)
        |> List.truncate 2
    rare
    |> List.collect (fun t -> ix.ByTokenState.TryFind(q.State, t) |> Option.defaultValue [])
    |> List.distinctBy (fun o -> o.Ein)
    |> List.map (fun o -> o, similarity ix q o)
    |> List.sortByDescending snd
    |> List.truncate k

let private uniqueOr (os: Org list) =
    match os |> List.distinctBy (fun o -> o.Ein) with
    | [] -> NoMatch
    | [ o ] -> Resolved o.Ein
    | many -> Ambiguous(many |> List.map (fun o -> o.Ein) |> List.truncate 10)

let rec resolve (ix: BmfIndex) (m: Method) (q: Query) : Outcome =
    match m with
    | ExactNameNational -> ix.ByExact.TryFind(exactKey q.Name) |> Option.defaultValue [] |> uniqueOr
    | ExactNameState -> ix.ByExactState.TryFind(exactKey q.Name, q.State) |> Option.defaultValue [] |> uniqueOr
    | ExactNameStateCityZip ->
        let hits = ix.ByExactState.TryFind(exactKey q.Name, q.State) |> Option.defaultValue []
        match hits |> List.distinctBy (fun o -> o.Ein) with
        | [ o ] -> Resolved o.Ein
        | [] -> NoMatch
        | many ->
            let byZip = many |> List.filter (fun o -> q.Zip5 <> "" && o.Zip5 = q.Zip5)
            let byCity = many |> List.filter (fun o -> String.Equals(o.City, q.City, StringComparison.OrdinalIgnoreCase))
            match byZip, byCity with
            | [ o ], _ -> Resolved o.Ein
            | _, [ o ] -> Resolved o.Ein
            | _ -> Ambiguous(many |> List.map (fun o -> o.Ein) |> List.truncate 10)
    | Cascade ->
        match resolve ix ExactNameStateCityZip q with
        | Resolved e -> Resolved e
        | first ->
            match resolve ix (FuzzyTfIdf(0.95, 0.20)) q with
            | Resolved e -> Resolved e
            | second ->
                let cands o = match o with Ambiguous cs -> cs | _ -> []
                match (cands first @ cands second) |> List.distinct with
                | [] -> NoMatch
                | cs -> Ambiguous(cs |> List.truncate 10)
    | FuzzyTfIdf(threshold, margin) ->
        match candidates ix q 5 with
        | [] -> NoMatch
        | (top, s1) :: rest ->
            let s2 = match rest with (_, s) :: _ -> s | [] -> 0.0
            if s1 >= threshold && s1 - s2 >= margin then Resolved top.Ein
            elif s1 >= 0.5 then Ambiguous((top :: (rest |> List.map fst)) |> List.map (fun o -> o.Ein))
            else NoMatch

type ResolutionScore =
    { Method: string
      Queries: int
      Resolved: int
      Correct: int
      Wrong: int
      Referred: int
      NoMatch: int
      Precision: float
      Coverage: float
      TruthInReferredCandidates: int } // oracle ceiling for an adjudicator choosing among candidates

let score (label: string) (ix: BmfIndex) (m: Method) (qs: Query list) =
    let outs = qs |> List.map (fun q -> q, resolve ix m q)
    let resolved = outs |> List.choose (fun (q, o) -> match o with Resolved e -> Some(q, e) | _ -> None)
    let correct = resolved |> List.filter (fun (q, e) -> e = q.FiledEin) |> List.length
    let referred = outs |> List.choose (fun (q, o) -> match o with Ambiguous cs -> Some(q, cs) | _ -> None)
    { Method = label
      Queries = qs.Length
      Resolved = resolved.Length
      Correct = correct
      Wrong = resolved.Length - correct
      Referred = referred.Length
      NoMatch = outs |> List.filter (fun (_, o) -> o = NoMatch) |> List.length
      Precision = if resolved.IsEmpty then 0.0 else float correct / float resolved.Length
      Coverage = float resolved.Length / float (max 1 qs.Length)
      TruthInReferredCandidates = referred |> List.filter (fun (q, cs) -> List.contains q.FiledEin cs) |> List.length }

// ---------------------------------------------------------------- V2 sanctions screening
type ListEntry = { Id: string; Name: string; EntryType: string; Program: string; Source: string }

/// Jaro-Winkler similarity (standard definition).
let jaroWinkler (a: string) (b: string) =
    if a = b then 1.0
    elif a.Length = 0 || b.Length = 0 then 0.0
    else
        let range = max 0 (max a.Length b.Length / 2 - 1)
        let aM = Array.create a.Length false
        let bM = Array.create b.Length false
        let mutable m = 0
        for i in 0 .. a.Length - 1 do
            let lo = max 0 (i - range)
            let hi = min (b.Length - 1) (i + range)
            let mutable j = lo
            let mutable found = false
            while not found && j <= hi do
                if not bM.[j] && a.[i] = b.[j] then
                    aM.[i] <- true; bM.[j] <- true; m <- m + 1; found <- true
                j <- j + 1
        if m = 0 then 0.0
        else
            let aS = [| for i in 0 .. a.Length - 1 do if aM.[i] then yield a.[i] |]
            let bS = [| for j in 0 .. b.Length - 1 do if bM.[j] then yield b.[j] |]
            let t = (Array.zip aS bS |> Array.filter (fun (x, y) -> x <> y) |> Array.length) / 2
            let mf = float m
            let jaro = (mf / float a.Length + mf / float b.Length + (mf - float t) / mf) / 3.0
            let prefix = Seq.zip a b |> Seq.takeWhile (fun (x, y) -> x = y) |> Seq.length |> min 4
            jaro + float prefix * 0.1 * (1.0 - jaro)

type ScreenIndex = { Entries: ListEntry list; ByToken: Map<string, ListEntry list> }

let buildScreenIndex (entries: ListEntry list) =
    { Entries = entries
      ByToken =
        entries
        |> List.collect (fun e -> keyTokens e.Name |> List.map (fun t -> t, e))
        |> List.groupBy fst |> List.map (fun (k, v) -> k, v |> List.map snd) |> Map.ofList }

/// Best list match for a name: candidates share a distinguishing token; score on the full normalised string.
let bestMatch (si: ScreenIndex) (name: string) =
    let key = exactKey name
    keyTokens name
    |> List.collect (fun t -> si.ByToken.TryFind t |> Option.defaultValue [])
    |> List.distinctBy (fun e -> e.Id + e.Name)
    |> List.map (fun e -> e, jaroWinkler key (exactKey e.Name))
    |> function [] -> None | xs -> Some(xs |> List.maxBy snd)

type ScreenResult = { Threshold: float; NamesScreened: int; Alerts: int; AlertsEntityTypeOnly: int; AlertsAfterTokenCoverageRule: int; AlertsByEntryType: (string * int) list; AlertsPersonLikeRecipient: int }

/// Token-coverage rule (deterministic secondary check): every distinguishing token of the LIST name must appear in the
/// recipient name. Removes alerts driven by one shared word (e.g. a single surname or place name).
let tokenCoverage (recipient: string) (listName: string) =
    let r = keyTokens recipient |> Set.ofList
    let l = keyTokens listName
    not l.IsEmpty && l |> List.forall r.Contains

/// Best match per name, computed once (in parallel; bestMatch is pure).
let matchAll (si: ScreenIndex) (names: string list) =
    names |> Array.ofList |> Array.Parallel.map (fun n -> n, bestMatch si n) |> List.ofArray

let screenMatched (matched: (string * (ListEntry * float) option) list) (threshold: float) =
    let hits = matched |> List.choose (fun (n, m) -> match m with Some(e, s) when s >= threshold -> Some(n, e, s) | _ -> None)
    { Threshold = threshold
      NamesScreened = matched.Length
      Alerts = hits.Length
      AlertsEntityTypeOnly = hits |> List.filter (fun (_, e, _) -> e.EntryType <> "individual" && e.EntryType <> "vessel" && e.EntryType <> "aircraft") |> List.length
      AlertsAfterTokenCoverageRule = hits |> List.filter (fun (n, e, _) -> tokenCoverage n e.Name) |> List.length
      AlertsByEntryType = hits |> List.countBy (fun (_, e, _) -> e.EntryType) |> List.sortBy fst
      // a recipient "name" that is only 2-3 tokens with no organisational word: typically a memorial fund or a person-named grantee line
      AlertsPersonLikeRecipient = hits |> List.filter (fun (n, _, _) -> let ts = tokens n in ts.Length <= 3 && keyTokens n = (ts |> List.filter (fun t -> t <> "THE"))) |> List.length }

// ---------------------------------------------------------------- loading (I/O edge)
let private splitCsv (line: string) = NetworkEconomics.splitCsv line

let loadBmf (dir: string) =
    [ "eo1.csv"; "eo2.csv"; "eo3.csv"; "eo4.csv" ]
    |> List.collect (fun f ->
        let p = Path.Combine(dir, f)
        if not (File.Exists p) then []
        else
            File.ReadLines p |> Seq.skip 1
            |> Seq.map splitCsv
            |> Seq.filter (fun r -> r.Length >= 14)
            |> Seq.map (fun r -> { Ein = r.[0]; Name = r.[1]; City = r.[4]; State = r.[5]; Zip5 = (if r.[6].Length >= 5 then r.[6].Substring(0, 5) else r.[6]); Subsection = r.[8]; Foundation = r.[13] })
            |> List.ofSeq)

let loadQueriesLine (line: string) =
    let r = splitCsv line
    { Name = r.[1]; City = r.[3]; State = r.[4]; Zip5 = r.[5]; FiledEin = r.[6] }

let loadQueries (path: string) =
    File.ReadLines path |> Seq.skip 1 |> Seq.map loadQueriesLine |> List.ofSeq

/// OFAC SDN (sdn.csv: ent_num,name,type,program,...) plus alt names (alt.csv: ent_num,alt_num,type,name,...) and consolidated.
let loadOfac (dir: string) =
    let clean (s: string) = s.Trim().Trim('"').Replace("-0-", "").Trim()
    let read f = let p = Path.Combine(dir, f) in if File.Exists p then File.ReadLines p |> Seq.map splitCsv |> List.ofSeq else []
    let prim source f =
        read f |> List.filter (fun r -> r.Length >= 4)
        |> List.map (fun r -> { Id = source + ":" + clean r.[0]; Name = clean r.[1]; EntryType = (match clean r.[2] with "" -> "entity" | t -> t.ToLowerInvariant()); Program = clean r.[3]; Source = source })
    let primaries = prim "SDN" "sdn.csv" @ prim "CONS" "cons_prim.csv"
    let typeOf = primaries |> List.map (fun e -> e.Id, e.EntryType) |> Map.ofList
    let alts source f =
        read f |> List.filter (fun r -> r.Length >= 4)
        |> List.map (fun r ->
            let id = source + ":" + clean r.[0]
            { Id = id; Name = clean r.[3]; EntryType = typeOf.TryFind id |> Option.defaultValue "entity"; Program = ""; Source = source + "-alt" })
    (primaries @ alts "SDN" "alt.csv" @ alts "CONS" "cons_alt.csv") |> List.filter (fun e -> e.Name <> "")

let screen (si: ScreenIndex) (names: string list) (threshold: float) = screenMatched (matchAll si names) threshold
