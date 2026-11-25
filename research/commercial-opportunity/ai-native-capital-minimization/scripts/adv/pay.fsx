#r "/tmp/claude-0/-home-user/45711cf3-dc26-5c8e-a6da-4af8bd5f0946/scratchpad/aincm/adv/work/aincm-copy/model/src/CapitalMinimization/bin/Release/net10.0/ServicingEconomics.dll"
open ServicingEconomics.Domain
open ServicingEconomics.Parameters
let s = sponsor "x" 4000.0 250000.0
let pay = s.Mix |> List.sumBy (fun a -> s.Accounts * a.ShareOfAccounts * a.Payments AiNative)
let ext = s.Mix |> List.sumBy (fun a -> s.Accounts * a.ShareOfAccounts * a.External AiNative)
printfn "payments passed through at 4,000 accounts: %.0f ; other external %.0f" pay ext
