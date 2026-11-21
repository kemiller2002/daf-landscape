module Daf.Enterprise.Tests.VettingTests

open Xunit
open Daf.Experiments.Vetting

let org ein name city state zip = { Ein = ein; Name = name; City = city; State = state; Zip5 = zip; Subsection = "03"; Foundation = "15" }

let ix =
    buildIndex
        [ org "111111111" "FIRST BAPTIST CHURCH" "SPRINGFIELD" "IL" "62701"
          org "222222222" "FIRST BAPTIST CHURCH" "PEORIA" "IL" "61602"
          org "333333333" "FIRST BAPTIST CHURCH" "AUSTIN" "TX" "73301"
          org "444444444" "SEATTLES UNION GOSPEL MISSION" "SEATTLE" "WA" "98111"
          org "555555555" "PATHWAYS FOR CHILDREN INC" "GLOUCESTER" "MA" "01930"
          org "666666666" "PATHFINDERS YOUTH LEAGUE" "BOSTON" "MA" "02108" ]

let q name city state zip ein = { Name = name; City = city; State = state; Zip5 = zip; FiledEin = ein }

[<Fact>]
let ``normalisation strips punctuation, maps synonyms and drops THE`` () =
    Assert.Equal("SAINT JUDE CHILDRENS RESEARCH HOSPITAL", exactKey "The St. Jude Children's Research Hospital")
    Assert.Equal<string list>([ "SAINT"; "JUDE"; "CHILDRENS"; "RESEARCH"; "HOSPITAL" ], keyTokens "St Jude Children's Research Hospital, Inc.")

[<Fact>]
let ``jaro-winkler matches the textbook values`` () =
    Assert.InRange(jaroWinkler "MARTHA" "MARHTA", 0.960, 0.962)
    Assert.InRange(jaroWinkler "DIXON" "DICKSONX", 0.812, 0.814)
    Assert.Equal(1.0, jaroWinkler "ABC" "ABC")
    Assert.Equal(0.0, jaroWinkler "" "ABC")

[<Fact>]
let ``a name shared nationally is ambiguous; state narrows; zip resolves`` () =
    let query = q "First Baptist Church" "Peoria" "IL" "61602" "222222222"
    Assert.True(match resolve ix ExactNameNational query with Ambiguous cs -> cs.Length = 3 | _ -> false)
    Assert.True(match resolve ix ExactNameState query with Ambiguous cs -> cs.Length = 2 | _ -> false)
    Assert.Equal(Resolved "222222222", resolve ix ExactNameStateCityZip query)

[<Fact>]
let ``punctuation differences defeat raw exact match but not normalised exact match`` () =
    Assert.Equal(Resolved "444444444", resolve ix ExactNameState (q "Seattle's Union Gospel Mission" "Seattle" "WA" "98111" "444444444"))

[<Fact>]
let ``fuzzy resolves a variant only with sufficient score and margin, otherwise refers or declines`` () =
    Assert.Equal(Resolved "555555555", resolve ix (FuzzyTfIdf(0.85, 0.10)) (q "Pathways for Children" "Gloucester" "MA" "01930" "555555555"))
    Assert.Equal(NoMatch, resolve ix (FuzzyTfIdf(0.85, 0.10)) (q "Totally Unknown Org" "Boston" "MA" "02108" "x"))

[<Fact>]
let ``scoring counts correct, wrong, referred and oracle candidate recall`` () =
    let qs = [ q "First Baptist Church" "Peoria" "IL" "61602" "222222222"; q "Pathways for Children Inc" "Gloucester" "MA" "01930" "555555555" ]
    let s = score "t" ix ExactNameState qs
    Assert.Equal(1, s.Resolved); Assert.Equal(1, s.Correct); Assert.Equal(1, s.Referred); Assert.Equal(1, s.TruthInReferredCandidates)

[<Fact>]
let ``token-coverage rule rejects alerts driven by one shared word`` () =
    Assert.False(tokenCoverage "Al Noor Islamic Center of Houston" "AL NOOR EXCHANGE COMPANY")   // EXCHANGE missing
    Assert.True(tokenCoverage "Example Trading Group Relief Fund" "EXAMPLE TRADING GROUP")
    let si = buildScreenIndex [ { Id = "1"; Name = "EXAMPLE TRADING GROUP"; EntryType = "entity"; Program = "X"; Source = "SDN" } ]
    let r = screen si [ "Example Trading Group"; "Example Hope Church" ] 0.9
    Assert.Equal(1, r.Alerts)

[<Fact>]
let ``cascade resolves deterministically first and falls back to fuzzy`` () =
    Assert.Equal(Resolved "222222222", resolve ix Cascade (q "First Baptist Church" "Peoria" "IL" "61602" "222222222"))
    Assert.Equal(Resolved "555555555", resolve ix Cascade (q "Pathways for Children" "Gloucester" "MA" "01930" "555555555"))
