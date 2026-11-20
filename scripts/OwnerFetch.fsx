// OwnerFetch.fsx: owner-run helper to collect the documents the agents could not fetch.
// F# port of scripts/owner_fetch.py (same tasks, same targets CSV, same output layout).
//
// Run it on YOUR OWN computer, not in the cloud session. It is a download assistant for a person:
// it opens each page in a visible browser and records what you save. It does not fill in or submit
// forms, solve CAPTCHAs or bot checks, hide that it is automation, or crawl beyond the named URLs.
//
// Modes per task
//   api      Regulations.gov official API (needs a free api.data.gov key in REGS_API_KEY).
//   direct   A known file URL (Wayback "id_" snapshots), fetched once through the browser context.
//   guided   Opens the start page; you navigate, fill any form yourself and click downloads. Enter
//            saves the downloads plus an .html and .mhtml snapshot of the page; "s" + Enter skips.
//   lookup   State charity registries (CA, NY): writes lookup-template.csv listing the top-50
//            sponsors; you search each one, fill the sheet, press Enter to save each result page,
//            and type "d" when finished.
//
// Setup (once):
//   Install the .NET 8 SDK: https://dotnet.microsoft.com/download
//   dotnet fsi scripts/OwnerFetch.fsx --install        # downloads Playwright's Chromium
//   export REGS_API_KEY=...                            # optional; https://api.data.gov/signup/
//
// Usage (from the repo root):
//   dotnet fsi scripts/OwnerFetch.fsx --list
//   dotnet fsi scripts/OwnerFetch.fsx --out owner-files --priority high
//   dotnet fsi scripts/OwnerFetch.fsx --out owner-files --targets-only --priority medium
//   dotnet fsi scripts/OwnerFetch.fsx --out owner-files --only regs-0242 candid-api-license
//
// Output: owner-files/<task_id>/... and owner-files/manifest.csv
//   (task_id, queue_item, kind, file, url, sha1, bytes, saved_at).
// Commit only what licences allow (the DAFRC report is CC BY; public comments and Wayback copies are
// fine). Keep copyrighted vendor reports local and paste the extracts needed.

#r "nuget: Microsoft.Playwright, 1.47.0"

open System
open System.Collections.Concurrent
open System.Collections.Generic
open System.IO
open System.Net.Http
open System.Security.Cryptography
open System.Text
open System.Text.Json
open Microsoft.Playwright

// ---------- types ----------

type Mode = Api | Direct | Guided | Lookup

type FetchTask = { TaskId: string; QueueItem: string; Mode: Mode; Url: string; Note: string }

type ManifestRow =
    { TaskId: string; QueueItem: string; Kind: string; File: string; Url: string
      Sha1: string; Bytes: int64; SavedAt: string }

type Options =
    { Out: string; Only: string list; ListOnly: bool; Targets: string; Priorities: string list
      TargetsOnly: bool; Profile: string; Install: bool }

// ---------- built-in tasks ----------

let docket = "IRS-2023-0053"
let wayback (ts: string) (url: string) = sprintf "https://web.archive.org/web/%sid_/%s" ts url

let regsTasks =
    [ 242 .. 254 ]
    |> List.map (fun n ->
        let id = sprintf "%s-%04d" docket n
        ({ TaskId = sprintf "regs-%04d" n; QueueItem = "P-B39N101-01"; Mode = Api; Url = id
           Note = sprintf "Public comment %s (2026 letter). Click the attachment's download button, then press Enter." id } : FetchTask))

let mkTask mode id q url note : FetchTask = { TaskId = id; QueueItem = q; Mode = mode; Url = url; Note = note }
let guided = mkTask Guided
let lookup = mkTask Lookup
let direct = mkTask Direct

let builtInTasks =
    regsTasks
    @ [ guided "dafgiving360-financials" "P-G0702-01" "https://www.dafgiving360.org/"
            "Find the FY2024 and FY2025 audited financial statements (About / Financials) and download both PDFs."
        guided "dafgiving360-policies" "P-B4428-01" "https://www.dafgiving360.org/"
            "Download the 2026 Program Policies PDF, then open the 'how to recommend a grant' help page and press Enter to snapshot it."
        guided "chariot-daf-reports" "P-B40N12-01; P-B40N1202-B43N2602-01"
            "https://www.givechariot.com/resources/webinars/2026-daf-fundraising-report-release"
            "Get the DAF Fundraising Report 2026 PDF (form: fill in yourself if you choose), and the 2024 and 2025 editions if offered."
        guided "mr-benchmarks-2026" "P-B40N12-01" "https://mrbenchmarks.com/"
            "Download the M+R Benchmarks 2026 PDF."
        guided "dafrc-reinventing-the-cycle" "P-B44N28-02"
            "https://scholarworks.iu.edu/dspace/discover?query=%22Reinventing+the+Cycle%22"
            "Open the DAF Research Collaborative report 'Reinventing the Cycle' (2025, CC BY) and download the PDF."
        guided "freewill-daf-reports" "P-B44N28-02" "https://www.freewill.com/"
            "Find and download the FreeWill 2025 and 2026 DAF Report PDFs."
        guided "candid-api-license" "P-B43N26-03-01" "https://candid.org/terms-of-service/api-license-agreement/"
            "Let the page load fully, then press Enter to snapshot it (need s.3.b.xi wording and any caching/retention clause)."
        guided "ncf-program-agreement" "P-B4222-020101-03" "https://secure.ncfgiving.com/agreement"
            "Let the agreement load, then press Enter to snapshot it (owner read for the robots-blocked NCF quotes)."
        guided "every-org-terms" "P-B43N26-03-02" "https://www.every.org/terms"
            "Press Enter to snapshot."
        guided "every-org-charity-api" "P-B43N26-03-02" "https://www.every.org/charity-api"
            "Press Enter to snapshot."
        lookup "ca-registry-top50" "P-B5002-01" "https://oag.ca.gov/charities"
            "Open the Registry Search from this page. For each sponsor in lookup-template.csv, search by name or EIN, fill status / latest filing year / notes in the CSV, and press Enter to save that result page."
        lookup "ny-registry-top50" "P-B5002-01" "https://charities-search.ag.ny.gov/RegistrySearch"
            "For each sponsor in lookup-template.csv, search by name or EIN (solve any CAPTCHA yourself), fill the CSV, and press Enter to save that result page."
        direct "wayback-rcf-1" "P-NPTREN-01"
            (wayback "20260316031245" "https://rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf")
            "RCF Donor User Guide, capture 2026-03-16."
        direct "wayback-rcf-2" "P-NPTREN-01"
            (wayback "20260722200822" "https://rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf")
            "RCF Donor User Guide, capture 2026-07-22."
        direct "wayback-ubs" "P-NPTREN-01"
            (wayback "20250421145451" "https://ubs.donorfirstx.com/pdf/UBS/UBS%20Donor%20User%20Guide.pdf")
            "UBS Donor User Guide, capture 2025-04-21." ]

// ---------- pure helpers: CSV ----------

/// RFC 4180 parser: quoted fields, doubled quotes, embedded commas and newlines.
let parseCsv (text: string) : string list list =
    let rec go i (field: StringBuilder) (row: string list) (rows: string list list) inQuotes =
        let endField () = field.ToString() :: row
        if i >= text.Length then
            let last = endField ()
            List.rev (if last = [ "" ] && row.IsEmpty then rows else List.rev last :: rows)
        else
            let c = text.[i]
            match inQuotes, c with
            | true, '"' when i + 1 < text.Length && text.[i + 1] = '"' -> go (i + 2) (field.Append '"') row rows true
            | true, '"' -> go (i + 1) field row rows false
            | true, _ -> go (i + 1) (field.Append c) row rows true
            | false, '"' -> go (i + 1) field row rows true
            | false, ',' -> go (i + 1) (StringBuilder()) (endField ()) rows false
            | false, '\r' -> go (i + 1) field row rows false
            | false, '\n' -> go (i + 1) (StringBuilder()) [] (List.rev (endField ()) :: rows) false
            | false, _ -> go (i + 1) (field.Append c) row rows false
    go 0 (StringBuilder()) [] [] false

let csvRecords (text: string) : Map<string, string> list =
    match parseCsv text with
    | header :: rows ->
        rows
        |> List.filter (fun r -> r <> [ "" ])
        |> List.map (fun r -> List.zip header (r @ List.replicate (max 0 (header.Length - r.Length)) "" |> List.take header.Length) |> Map.ofList)
    | [] -> []

let csvEscape (s: string) =
    if s.IndexOfAny([| ','; '"'; '\n'; '\r' |]) >= 0 then "\"" + s.Replace("\"", "\"\"") + "\"" else s

let csvLine (fields: string list) = fields |> List.map csvEscape |> String.concat ","

let get (key: string) (m: Map<string, string>) = m |> Map.tryFind key |> Option.defaultValue ""

// ---------- pure helpers: misc ----------

let sha1Hex (data: byte[]) =
    use h = SHA1.Create()
    h.ComputeHash data |> Array.map (fun b -> b.ToString "x2") |> String.concat ""

let nowIso () = DateTimeOffset.UtcNow.ToString "yyyy-MM-ddTHH:mm:ssK"

let safeName (s: string) =
    let cleaned = s |> String.map (fun c -> if Char.IsLetterOrDigit c || c = '.' || c = '_' || c = '-' then c else '_')
    let cut = if cleaned.Length > 150 then cleaned.Substring(0, 150) else cleaned
    if String.IsNullOrEmpty cut then "file" else cut

let manifestRow (t: FetchTask) (kind: string) (path: string) (url: string) : ManifestRow =
    let data = File.ReadAllBytes path
    { TaskId = t.TaskId; QueueItem = t.QueueItem; Kind = kind; File = path; Url = url
      Sha1 = sha1Hex data; Bytes = int64 data.Length; SavedAt = nowIso () }

let regsAttachmentUrls (payload: JsonElement) : string list =
    match payload.TryGetProperty "included" with
    | true, inc when inc.ValueKind = JsonValueKind.Array ->
        [ for a in inc.EnumerateArray() do
            match a.TryGetProperty "attributes" with
            | true, attrs ->
                match attrs.TryGetProperty "fileFormats" with
                | true, ff when ff.ValueKind = JsonValueKind.Array ->
                    for f in ff.EnumerateArray() do
                        match f.TryGetProperty "fileUrl" with
                        | true, u when u.ValueKind = JsonValueKind.String -> yield u.GetString()
                        | _ -> ()
                | _ -> ()
            | _ -> () ]
    | _ -> []

// ---------- targets CSV (owner-fetch-targets) ----------

let targetsCsvDefault = "data/mission-2026-11-14/owner-fetch-targets-2026-11-20.csv"
let priorityRank = function "high" -> 0 | "medium" -> 1 | "low" -> 2 | _ -> 9

let modeOfTarget = function "lookup" -> Lookup | _ -> Guided   // downloads also open in the visible browser

let taskOfTarget (r: Map<string, string>) : FetchTask =
    { TaskId = get "target_id" r; QueueItem = get "needed_for" r; Mode = modeOfTarget (get "mode" r)
      Url = get "url" r
      Note = sprintf "[%s] %s (blocked: %s)" (get "priority" r) (get "what_to_get" r) (get "block_reason" r) }

let targetsFromRecords (priorities: string list) (rows: Map<string, string> list) =
    let alreadyCovered r =
        let v = (get "already_in_owner_fetch" r).Trim().ToLowerInvariant()
        v.StartsWith "y" || v.StartsWith "true"
    rows
    |> List.filter (fun r ->
        not (alreadyCovered r)
        && (get "url" r).StartsWith "http"
        && (priorities.IsEmpty || List.contains (get "priority" r) priorities))
    |> List.sortBy (fun r -> priorityRank (get "priority" r), get "target_id" r)
    |> List.map taskOfTarget

let loadTargets (path: string) (priorities: string list) =
    if String.IsNullOrEmpty path || not (File.Exists path) then []
    else File.ReadAllText path |> csvRecords |> targetsFromRecords priorities

// ---------- lookup template ----------

let regCsv = "data/mission-2026-11-14/state-registration-2026-11-20.csv"
let lookupCols =
    [ "ein"; "sponsor_name"; "fy2024_rank_assets"; "status"; "registry_id"; "latest_filing_year"
      "enforcement_notice"; "notes"; "looked_up_on" ]

let top50Sponsors (rows: Map<string, string> list) =
    let rank r = match Double.TryParse(get "fy2024_rank_assets" r) with | true, v -> v | _ -> 9999.0
    rows
    |> List.filter (fun r -> get "size_band_fy2024" r = "top50")
    |> List.distinctBy (get "ein")
    |> List.sortBy rank

let templateLines (sponsors: Map<string, string> list) =
    csvLine lookupCols
    :: (sponsors
        |> List.map (fun s ->
            lookupCols
            |> List.map (fun c ->
                match c with
                | "ein" | "sponsor_name" | "fy2024_rank_assets" -> get c s
                | _ -> "")
            |> csvLine))

// ---------- side effects ----------

let appendManifest (out: string) (rows: ManifestRow list) =
    if not rows.IsEmpty then
        let path = Path.Combine(out, "manifest.csv")
        let header = csvLine [ "task_id"; "queue_item"; "kind"; "file"; "url"; "sha1"; "bytes"; "saved_at" ]
        let lines =
            rows |> List.map (fun r ->
                csvLine [ r.TaskId; r.QueueItem; r.Kind; r.File; r.Url; r.Sha1; string r.Bytes; r.SavedAt ])
        let prefix = if File.Exists path then [] else [ header ]
        File.AppendAllLines(path, prefix @ lines)

let taskFolder (out: string) (t: FetchTask) =
    Directory.CreateDirectory(Path.Combine(out, t.TaskId)).FullName

let prompt (text: string) =
    printf "%s" text
    (Console.ReadLine() |> Option.ofObj |> Option.defaultValue "").Trim().ToLowerInvariant()

let runApi (http: HttpClient) (key: string) (out: string) (t: FetchTask) =
    task {
        let folder = taskFolder out t
        use req = new HttpRequestMessage(HttpMethod.Get, sprintf "https://api.regulations.gov/v4/comments/%s?include=attachments" t.Url)
        req.Headers.Add("X-Api-Key", key)
        let! resp = http.SendAsync req
        resp.EnsureSuccessStatusCode() |> ignore
        let! meta = resp.Content.ReadAsByteArrayAsync()
        let metaPath = Path.Combine(folder, "comment.json")
        File.WriteAllBytes(metaPath, meta)
        let urls = regsAttachmentUrls (JsonDocument.Parse(meta).RootElement.Clone())
        let saved = ResizeArray<ManifestRow>()
        for u in urls do
            do! Threading.Tasks.Task.Delay 1500                      // stay well inside api.data.gov limits
            let! bytes = http.GetByteArrayAsync u
            let p = Path.Combine(folder, safeName (u.Substring(u.LastIndexOf '/' + 1)))
            File.WriteAllBytes(p, bytes)
            saved.Add(manifestRow t "api_attachment" p u)
        return manifestRow t "api_metadata" metaPath t.Url :: List.ofSeq saved
    }

let runDirect (context: IBrowserContext) (out: string) (t: FetchTask) =
    task {
        let folder = taskFolder out t
        let! resp = context.APIRequest.GetAsync(t.Url, APIRequestContextOptions(Timeout = Nullable 120000.0f))
        if not resp.Ok then
            printfn "  ! HTTP %d for %s" resp.Status t.Url
            return []
        else
            let! body = resp.BodyAsync()
            let p = Path.Combine(folder, safeName (t.Url.Substring(t.Url.LastIndexOf '/' + 1)))
            File.WriteAllBytes(p, body)
            return [ manifestRow t "direct" p t.Url ]
    }

let snapshot (page: IPage) (folder: string) (t: FetchTask) =
    task {
        let! html = page.ContentAsync()
        let htmlPath = Path.Combine(folder, "page.html")
        File.WriteAllText(htmlPath, html, Encoding.UTF8)
        let htmlRow = manifestRow t "page_html" htmlPath page.Url
        try
            let! cdp = page.Context.NewCDPSessionAsync page
            let args = Dictionary<string, obj>(dict [ "format", box "mhtml" ])
            let! result = cdp.SendAsync("Page.captureSnapshot", args)
            match Option.ofNullable result with
            | Some r ->
                let mhtmlPath = Path.Combine(folder, "page.mhtml")
                File.WriteAllText(mhtmlPath, r.GetProperty("data").GetString(), Encoding.UTF8)
                return [ htmlRow; manifestRow t "page_mhtml" mhtmlPath page.Url ]
            | None -> return [ htmlRow ]
        with ex ->
            printfn "  (mhtml snapshot skipped: %s)" ex.Message
            return [ htmlRow ]
    }

/// Downloads are queued as they start and saved after you press Enter
/// (saving inside the event handler can deadlock Playwright's dispatcher).
let saveDownloads (folder: string) (t: FetchTask) (queue: ConcurrentQueue<IDownload>) =
    task {
        let rows = ResizeArray<ManifestRow>()
        for d in queue.ToArray() do
            let p = Path.Combine(folder, safeName d.SuggestedFilename)
            do! d.SaveAsAsync p
            printfn "  saved %s" (Path.GetFileName p)
            rows.Add(manifestRow t "download" p d.Url)
        return List.ofSeq rows
    }

let startUrl (t: FetchTask) =
    match t.Mode with
    | Api -> sprintf "https://www.regulations.gov/comment/%s" t.Url   // no API key: open the comment page
    | _ -> t.Url

let runGuided (context: IBrowserContext) (out: string) (t: FetchTask) =
    task {
        let folder = taskFolder out t
        let! page = context.NewPageAsync()
        let queue = ConcurrentQueue<IDownload>()
        page.Download.Add(fun d -> queue.Enqueue d)
        let! _ = page.GotoAsync(startUrl t, PageGotoOptions(WaitUntil = Nullable WaitUntilState.DOMContentLoaded))
        printfn "  %s" t.Note
        let answer = prompt "  Enter = done and snapshot page, s = skip: "
        let! downloads = saveDownloads folder t queue
        let! snap = if answer = "s" then Threading.Tasks.Task.FromResult [] else snapshot page folder t
        do! page.CloseAsync()
        return downloads @ snap
    }

let writeTemplate (folder: string) =
    let path = Path.Combine(folder, "lookup-template.csv")
    if not (File.Exists path) then                                     // never overwrite the owner's sheet
        let sponsors = if File.Exists regCsv then File.ReadAllText regCsv |> csvRecords |> top50Sponsors else []
        File.WriteAllLines(path, templateLines sponsors)
    path

let runLookup (context: IBrowserContext) (out: string) (t: FetchTask) =
    task {
        let folder = taskFolder out t
        let tpl = writeTemplate folder
        printfn "  Template: %s  (fill it in as you go)" tpl
        let! page = context.NewPageAsync()
        let queue = ConcurrentQueue<IDownload>()
        page.Download.Add(fun d -> queue.Enqueue d)
        let! _ = page.GotoAsync(t.Url, PageGotoOptions(WaitUntil = Nullable WaitUntilState.DOMContentLoaded))
        printfn "  %s" t.Note
        let rows = ResizeArray<ManifestRow>()
        let n = ref 0
        let finished = ref false
        while not finished.Value do
            if prompt "  Enter = save this result page, d = done: " = "d" then finished.Value <- true
            else
                n.Value <- n.Value + 1
                let sub = Directory.CreateDirectory(Path.Combine(folder, sprintf "result-%03d" n.Value)).FullName
                let! snap = snapshot page sub t
                rows.AddRange snap
        let! downloads = saveDownloads folder t queue
        do! page.CloseAsync()
        return List.ofSeq rows @ downloads @ [ manifestRow t "lookup_template" tpl t.Url ]
    }

// ---------- CLI ----------

let rec parseArgs (o: Options) (args: string list) =
    let takeValues rest = rest |> List.takeWhile (fun (a: string) -> not (a.StartsWith "--"))
    match args with
    | [] -> o
    | "--out" :: v :: rest -> parseArgs { o with Out = v } rest
    | "--only" :: rest -> let vs = takeValues rest in parseArgs { o with Only = vs } (List.skip vs.Length rest)
    | "--priority" :: rest -> let vs = takeValues rest in parseArgs { o with Priorities = vs } (List.skip vs.Length rest)
    | "--targets" :: v :: rest -> parseArgs { o with Targets = v } rest
    | "--profile" :: v :: rest -> parseArgs { o with Profile = v } rest
    | "--list" :: rest -> parseArgs { o with ListOnly = true } rest
    | "--targets-only" :: rest -> parseArgs { o with TargetsOnly = true } rest
    | "--install" :: rest -> parseArgs { o with Install = true } rest
    | unknown :: rest -> eprintfn "ignoring unknown argument: %s" unknown; parseArgs o rest

let defaults =
    { Out = "owner-files"; Only = []; ListOnly = false; Targets = targetsCsvDefault; Priorities = []
      TargetsOnly = false; Install = false
      Profile = Path.Combine(Environment.GetFolderPath Environment.SpecialFolder.UserProfile, ".daf-owner-fetch-profile") }

let selectTasks (o: Options) =
    let extra = loadTargets o.Targets o.Priorities
    let all = if o.TargetsOnly then extra else builtInTasks @ extra
    if o.Only.IsEmpty then all else all |> List.filter (fun t -> List.contains t.TaskId o.Only)

let modeName = function Api -> "api" | Direct -> "direct" | Guided -> "guided" | Lookup -> "lookup"

let main (argv: string list) =
    let o = parseArgs defaults argv
    if o.Install then
        exit (Microsoft.Playwright.Program.Main [| "install"; "chromium" |])
    let tasks = selectTasks o
    if o.ListOnly then
        tasks |> List.iter (fun t -> printfn "%-30s %-7s %-28s %s" t.TaskId (modeName t.Mode) t.QueueItem t.Url)
        0
    else
        Directory.CreateDirectory o.Out |> ignore
        let key = Environment.GetEnvironmentVariable "REGS_API_KEY" |> Option.ofObj |> Option.defaultValue ""
        let viaApi, viaBrowser = tasks |> List.partition (fun t -> t.Mode = Api && key <> "")
        use http = new HttpClient(Timeout = TimeSpan.FromSeconds 60.0)
        for t in viaApi do
            printfn "[api] %s" t.TaskId
            try appendManifest o.Out ((runApi http key o.Out t).GetAwaiter().GetResult())
            with ex -> printfn "  ! %s; unset REGS_API_KEY to use the browser for this one" ex.Message
        if not viaBrowser.IsEmpty then
            use pw = Playwright.CreateAsync().GetAwaiter().GetResult()
            let context =
                pw.Chromium.LaunchPersistentContextAsync(
                    o.Profile, BrowserTypeLaunchPersistentContextOptions(Headless = Nullable false, AcceptDownloads = Nullable true))
                  .GetAwaiter().GetResult()
            for t in viaBrowser do
                printfn "[%s] %s  (%s)" (modeName t.Mode) t.TaskId t.QueueItem
                let run =
                    match t.Mode with
                    | Direct -> runDirect context o.Out t
                    | Lookup -> runLookup context o.Out t
                    | _ -> runGuided context o.Out t
                appendManifest o.Out (run.GetAwaiter().GetResult())
            context.CloseAsync().GetAwaiter().GetResult()
        printfn "Done. Manifest: %s" (Path.Combine(o.Out, "manifest.csv"))
        0

// fsi.CommandLineArgs.[0] is the script path.
exit (main (fsi.CommandLineArgs |> Array.toList |> List.tail))
