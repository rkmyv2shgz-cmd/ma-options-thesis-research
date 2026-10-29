# M&A option-market response and defensive-hedging study — reproduction guide

This is the research companion to the thesis *Option-Market Signals and Hedging Strategies for Deal-Completion Risk in Mergers and Acquisitions*.

## What the thesis does, and does not, claim

The research question is how option markets respond to M&A news and whether defensive puts/collars can cushion target-shareholder losses. This study does **not** estimate which merger will fail. The two cases are a completed cash transaction (Cisco/Splunk) and a terminated transaction (Tapestry/Capri).

The main empirical evidence has three different provenances:

1. `ma_thesis.ipynb`: a saved QuantConnect Research notebook whose principal code cell has executed outputs. The QuantConnect US Equity Option Universe supplies vendor/model-derived IV, Greeks, option volume and open interest, **not a matched exchange-bid/ask execution tape**. This notebook needs QuantConnect data access to re-execute.
2. `OptionChain_CPRI 20-Dec-24_20241023.csv` and `...20241024.csv`: historical December 20, 2024 CPRI option-chain exports uploaded by the thesis author from Market Chameleon. The 25 October observation is **not a CSV**, but a manually transcribed historical-chain screenshot from the author.
3. `benchmark_event_study.py`: transcribed CPRI daily underlying close figures for October 21–November 15, 2024 based on user-supplied Barchart images, paired with FRED's S&P 500 daily index. The source table is present explicitly in the code. The 19-return reference-window rank is descriptive, not a valid broad-population hypothesis test.

Historical contract quotations can be stale or asynchronous, and US equity options generally permit early exercise. Quoted midpoint option spreads are not guaranteed executable prices and are not automatically state probabilities.

## Recreate the numeric tables and diagnostics

Using Python 3.10+:

```bash
python -m pip install -r requirements.txt
python reproduce_cpri.py 'OptionChain_CPRI 20-Dec-24_20241023.csv' 'OptionChain_CPRI 20-Dec-24_20241024.csv' --output cpri_vertical_reproduced.csv
python quote_quality_and_iv.py
python benchmark_event_study.py
python quoted_hedges.py 'OptionChain_CPRI 20-Dec-24_20241023.csv'
```

The quote-quality Python diagnostic uses European Black–Scholes only as a **sensitivity check**, not as an appropriate American-option execution/pricing engine. The non-crossed quote check is not a put–call parity arbitrage test. The risk-free rate used for the diagnostic is the explicitly **illustrative** continuous rate `R=0.05`; 2024 historical curve calibration is not claimed.

## Parameters and calculation boundaries

- CPRI observation days: 2024-10-23, 2024-10-24 (CSV); 2024-10-25 (screenshot only).
- Fixed CPRI put-vertical maturity: 2024-12-20; long put `K_H=40`, short put `K_L=35`; source quote snapshot displayed at **15:59:30 US Eastern**, but leg-level exchange timestamps and sizes are unavailable.
- Historical CPRI screenshot share prices: 41.81 (Oct 23), 41.53 (Oct 24), 21.25 (Oct 25). The separate Barchart end-of-day close series has 41.60 for Oct 24 and 21.26 for Oct 25. The two sources need not agree to the penny because snapshots and closing-price definitions differ.
- 23 October quotes from CSV: $40 put bid 7.10, ask 8.30; $35 put bid 5.80, ask 6.40; $45 call bid 6.30 (with **zero reported contract volume** on this day).
- 25 October screenshot: $40 put bid 18.60, ask 18.90; $35 put bid 13.70, ask 14.00; $45 call ask 0.15.
- Indicative 23-to-25 October strategies: long stock alone, stock plus $40 put, stock plus put and short $45 call. All contract legs are assumed opened/closed at their displayed opposite-side quotes; without synchronized executable quotes this is **not** a historical executed-trade backtest. Fees, funding and dividends are ignored over the two-session horizon.
- The **theoretical** discounted two-state illustration assumes S0=82, success S=100, failure S=60, continuously compounded r=5%, T=0.5 years, no dividend. The derived Q failure weight is approximately 39.81%. Hypothetical physical completion probabilities in a sensitivity table are **not empirically calibrated**. No VaR/CVaR estimate under P is claimed.
- Five-outcome terminal stress prices are 35, 60, 80, 100, 110, as an illustrative deterministic stress without assigned state probabilities.
- Executed QuantConnect notebook filters and constants are defined in its main code cell, including thresholds for IV, delta, open interest, and expiry selection. These may remove economically interesting observations, so no filtered-sample put–call parity inference is claimed.

## Data rights and publication

The author-provided historical CSVs are included in the **private review package** for reproducibility. **Do not upload vendor-owned raw CSVs publicly unless the provider's licence permits redistribution.** The separate GitHub-ready source-code ZIP intentionally omits raw proprietary market-data files. A public GitHub repository has not been created or verified, so no public repository link appears in the thesis.

## References

- QuantConnect, US Equity Option Universe: https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/quantconnect/us-equity-option-universe
- Market Chameleon: https://marketchameleon.com/
- Barchart historical options: https://www.barchart.com/options/price-history
- FRED S&P 500: https://fred.stlouisfed.org/series/SP500
