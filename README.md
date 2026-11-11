# M&A option-market response and defensive-hedging study — reproduction guide

This is the research companion to the thesis *Option-Market Signals and Hedging Strategies for Deal-Completion Risk in Mergers and Acquisitions*.

## What the thesis does, and does not, claim

The research question is how option markets respond to M&A news and whether defensive puts/collars can cushion target-shareholder losses. This study does **not** estimate which merger will fail. The two cases are a completed cash transaction (Cisco/Splunk) and a terminated transaction (Tapestry/Capri).

The main empirical evidence has three different provenances:

1. `ma_thesis.ipynb`: a saved QuantConnect Research notebook whose principal code cell has executed outputs. The QuantConnect US Equity Option Universe supplies vendor/model-derived IV, Greeks, option volume and open interest, **not a matched exchange-bid/ask execution tape**. This notebook needs QuantConnect data access to re-execute.
2. `OptionChain_CPRI 20-Dec-24_20241023.csv`, `...20241024.csv`, and `...20241025.csv`: three **author-downloaded Market Chameleon historical option-chain CSV exports** for the December 20, 2024 maturity. All three quoted option panels are now source-file verified; the corresponding underlying spot snapshots come from the author's archived Market Chameleon screenshots. Original vendor CSV files are not redistributed publicly.
3. `benchmark_event_study.py`: transcribed CPRI daily underlying close figures for October 21–November 15, 2024 based on user-supplied Barchart images, paired with FRED's S&P 500 daily index. The source table is present explicitly in the code. The 19-return reference-window rank is descriptive, not a valid broad-population hypothesis test.

Historical contract quotations can be stale or asynchronous, and US equity options generally permit early exercise. Quoted midpoint option spreads are not guaranteed executable prices and are not automatically state probabilities.

## Selected CPRI Market Chameleon data (public summary)

For a concise, inspectable display of the option-chain observations used in the thesis:

- **[CPRI quotation table — 23, 24 and 25 October 2024](data/README.md):** selected bid/ask prices, underlying stock prices, put-spread midpoint and quote-side ranges, with provenance and execution caveats.
- **[Selected quotation CSV](data/cpri_selected_quotes.csv):** machine-readable version of the table for checking the calculations.
- **[Put-spread chart](figures/cpri_put_spread.svg):** visual summary showing the repricing and the theoretical $5 terminal payoff cap.

The 23, 24 and **25 October option quotation values are verified against original author-downloaded Market Chameleon CSV exports**. Underlying spot snapshots are sourced separately from historical-chain screenshots. This GitHub repository does **not** contain full vendor market-data exports; code that reads them requires separately obtained, appropriately licensed input files.

## Recreate the numeric tables and diagnostics

Using Python 3.10+:

```bash
python -m pip install -r requirements.txt
python reproduce_cpri.py 'OptionChain_CPRI 20-Dec-24_20241023.csv' 'OptionChain_CPRI 20-Dec-24_20241024.csv' 'OptionChain_CPRI 20-Dec-24_20241025.csv' --output cpri_vertical_reproduced.csv
python quote_quality_and_iv.py
python benchmark_event_study.py
python quoted_hedges.py 'OptionChain_CPRI 20-Dec-24_20241023.csv' 'OptionChain_CPRI 20-Dec-24_20241025.csv'
```

The quote-quality Python diagnostic uses European Black–Scholes only as a **sensitivity check**, not as an appropriate American-option execution/pricing engine. The non-crossed quote check is not a put–call parity arbitrage test. The risk-free rate used for the diagnostic is the explicitly **illustrative** continuous rate `R=0.05`; 2024 historical curve calibration is not claimed.

## Parameters and calculation boundaries

- CPRI option-quote observation days: 2024-10-23, 2024-10-24 and 2024-10-25, each supported by an original Market Chameleon CSV download. The displayed underlying-spot snapshots are taken from the archived provider screenshots.
- Fixed CPRI put-vertical maturity: 2024-12-20; long put `K_H=40`, short put `K_L=35`; source quote snapshot displayed at **15:59:30 US Eastern**, but leg-level exchange timestamps and sizes are unavailable.
- Historical CPRI screenshot share prices: 41.81 (Oct 23), 41.53 (Oct 24), 21.25 (Oct 25). The separate Barchart end-of-day close series has 41.60 for Oct 24 and 21.26 for Oct 25. The two sources need not agree to the penny because snapshots and closing-price definitions differ.
- 23 October quotes from CSV: $40 put bid 7.10, ask 8.30; $35 put bid 5.80, ask 6.40; $45 call bid 6.30 (with **zero reported contract volume** on this day).
- 25 October original CSV: $40 put bid 18.60, ask 18.90 (volume 12); $35 put bid 13.70, ask 14.00 (volume 301); $45 call bid 0.05, ask 0.15 (volume 162). These exactly match the previously transcribed quoted prices.
- Indicative 23-to-25 October strategies: long stock alone, stock plus $40 put, stock plus put and short $45 call. All contract legs are assumed opened/closed at their displayed opposite-side quotes; without synchronized executable quotes this is **not** a historical executed-trade backtest. Fees, funding and dividends are ignored over the two-session horizon.
- The **theoretical** discounted two-state illustration assumes S0=82, success S=100, failure S=60, continuously compounded r=5%, T=0.5 years, no dividend. The derived Q failure weight is approximately 39.81%. Hypothetical physical completion probabilities in a sensitivity table are **not empirically calibrated**. No VaR/CVaR estimate under P is claimed.
- Five-outcome terminal stress prices are 35, 60, 80, 100, 110, as an illustrative deterministic stress without assigned state probabilities.
- Executed QuantConnect notebook filters and constants are defined in its main code cell, including thresholds for IV, delta, open interest, and expiry selection. These may remove economically interesting observations, so no filtered-sample put–call parity inference is claimed.

## Data rights and publication

The three author-provided historical CSV downloads are retained privately for verification, not uploaded to this public repository. **Do not upload vendor-owned raw CSVs publicly unless the provider's licence permits redistribution.** The public research repository is https://github.com/rkmyv2shgz-cmd/ma-options-thesis-research . The thesis reproducibility appendix should link here; its October 25 data-provenance description should be updated to reflect the newly received original CSV.

## References

- QuantConnect, US Equity Option Universe: https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/quantconnect/us-equity-option-universe
- Market Chameleon: https://marketchameleon.com/
- Barchart historical options: https://www.barchart.com/options/price-history
- FRED S&P 500: https://fred.stlouisfed.org/series/SP500
