/// Model 5: migration and licensing revenue per customer, and the minimum viable DAF programme grid (port of agent
/// CD's data/evidence/CD/mvp.py, P3-ASM-CD001..CD008). Pure.
module CompetitiveAdvantageCreation.Licensing

/// Programme economics at the programme (entity 3), not at Echelon Foundry.
type GridRow =
    { HostModel: string
      FixedCase: string
      FixedUsd: float
      VarCase: string
      VarUsd: float
      AvgBalance: float
      FeeRate: float
      MarginPerAccount: float
      BreakEvenAccounts: int option
      BreakEvenAua: float option }

/// Break-even accounts = ceil(fixed / (balance x fee - variable)); never when the margin is not positive.
let breakEven (fixedUsd: float) (varUsd: float) (balance: float) (fee: float) =
    let m = balance * fee - varUsd
    let n = if m > 0.0 then Some(int (ceil (fixedUsd / m))) else None
    m, n, n |> Option.map (fun k -> float k * balance)

/// Full grid in CD's order: host model x fixed case x variable case x balance x fee.
let grid (fixedByHost: (string * (string * float) list) list) (variable: (string * float) list) (balances: float list) (fees: float list) : GridRow list =
    [ for host, fixeds in fixedByHost do
          for fk, fv in fixeds do
              for vk, vv in variable do
                  for b in balances do
                      for f in fees do
                          let m, n, aua = breakEven fv vv b f
                          { HostModel = host; FixedCase = fk; FixedUsd = fv; VarCase = vk; VarUsd = vv; AvgBalance = b; FeeRate = f
                            MarginPerAccount = m; BreakEvenAccounts = n; BreakEvenAua = aua } ]

/// Vendor licence revenue for one customer: accounts x net price, floored at a minimum annual fee.
let licenceRevenue (accounts: float) (pricePerAccount: float) (minimumFee: float) (partnerShare: float) =
    max (accounts * pricePerAccount) minimumFee * (1.0 - partnerShare)

/// Accounts a customer needs before the per-account price exceeds the minimum fee.
let accountsAboveMinimum (pricePerAccount: float) (minimumFee: float) =
    if pricePerAccount > 0.0 then minimumFee / pricePerAccount else infinity

/// Programme-level fee income versus the vendor's licence take: how much of the programme's revenue the licence uses.
let licenceShareOfProgrammeFees (accounts: float) (balance: float) (feeRate: float) (licence: float) =
    let fees = accounts * balance * feeRate
    if fees > 0.0 then Some(licence / fees) else None

/// Migration revenue for an engagement: assessment fee plus an implementation fee recovering a share of the cost.
let migrationRevenue (assessmentFee: float) (implementationCost: float) (recoveryShare: float) =
    assessmentFee + implementationCost * recoveryShare
