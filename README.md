# Leveraged Treasury ETF Trading Strategies

Python research repo for COMP0051 (UCL) that investigates **leveraged momentum
vs. mean‑reversion** approaches on the SPDR Portfolio Long‑Term Treasury ETF
(**SPTL**) during 2023.

## Highlights
- **Strategies implemented**
  - *MACD Momentum* (12/26‑EMA crossover)
  - *Bollinger‑Band Mean Reversion*  
- **Leverage 10 ×** with dynamic capital‑account growth.
- **Risk metrics:** Sharpe, Calmar, drawdowns.
- End‑to‑end pipeline: raw data → back‑test → matplotlib PnL plots → PDF report.

| Strategy | Final Equity | Sharpe | Calmar |
|----------|-------------:|-------:|-------:|
| MACD     | \$67 k       | 0.58   | 0.87   |
| BBMR     | \$1.29 m     | **2.84** | **4.12** |
