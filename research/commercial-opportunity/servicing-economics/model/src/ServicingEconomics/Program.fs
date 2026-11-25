module ServicingEconomics.Program

open System.IO
open ServicingEconomics.Domain

[<EntryPoint>]
let main argv =
    let outDir = if argv.Length > 0 then argv.[0] else "out"
    Directory.CreateDirectory outDir |> ignore
    let r = Economics.evaluate Parameters.h0Org Parameters.h0Activities Conventional (Parameters.price 20.0) noStress [ Parameters.uniformSponsor "H0" 1.0e9 200000.0 ]
    printfn "H0 at $1B, B=$200k, 20 bps: revenue %.0f cost %.0f profit %.0f" r.Revenue r.TotalCost r.OperatingProfit
    0
