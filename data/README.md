# Selected CPRI historical option quotations — thesis data summary

These are **selected strike quotations** for the December 20, 2024 Capri Holdings (CPRI) equity-option expiration, compiled from the thesis author's **three original Market Chameleon historical-chain CSV downloads** dated 23, 24 and 25 October 2024. The **underlying spot figures** are taken from the author’s corresponding archived Market Chameleon historical-chain screenshots: they are not fields contained in the CSV exports.

This is a compact secondary research table, **not** the original full historical option-chain export. Licensed full vendor CSVs are not publicly redistributed.

## Selected quotations (USD per share)

| Date | CPRI spot (screenshot) | $40 put bid/ask (CSV) | $35 put bid/ask (CSV) | $40/$35 put vertical midpoint | Two-leg quoted sale / purchase side |
|---|---:|---:|---:|---:|---:|
| 2024-10-23 | 41.81 | 7.10 / 8.30 | 5.80 / 6.40 | **1.60** | 0.70 / 2.50 |
| 2024-10-24 | 41.53 | 6.80 / 8.30 | 5.80 / 6.00 | **1.65** | 0.80 / 2.50 |
| 2024-10-25 | 21.25 | 18.60 / 18.90 | 13.70 / 14.00 | **4.90** | 4.60 / 5.20 |

The $45 call used in the indicative collar comparison is also verified from the CSVs: **23 October bid $6.30, volume 0**; **25 October ask $0.15, volume 162**. The $40 put's 25 October volume is 12; the $35 put's 25 October volume is 301. These values are daily displayed volumes, not evidence that the indicated bid/ask sizes were executable.

## Source and interpretation

- **Option prices, volumes, open interest and strikes:** author-downloaded Market Chameleon historical option-chain CSVs, with exact observation dates 2024-10-23, 2024-10-24 and 2024-10-25, all for the 20-Dec-2024 expiry.
- **Underlying spot at the quoted snapshot:** author-supplied Market Chameleon historical-chain screenshots (the option CSVs omit spot).
- **CSV [selected summary](cpri_selected_quotes.csv):** derived from the three source exports and the displayed spot observations.
- **Chart [put vertical around the injunction](../figures/cpri_put_spread.svg):** midpoint and quoted-side ranges. The error bars are quote ranges, **not confidence intervals**.

For long $40 put / short $35 put, the midpoint is `(P40_bid + P40_ask)/2 - (P35_bid + P35_ask)/2`. Quoted sale and purchase sides are `P40_bid - P35_ask` and `P40_ask - P35_bid`. The October 25 quote-side purchase value **$5.20 exceeds the $5 terminal payoff cap**. It should not be interpreted as a viable executed vertical; quotes are not necessarily contemporaneous or executable. The spread value divided by width is **not** a verified failure probability.

## Replication

The research scripts now accept all three **original downloaded CSV** files (not this compact derived summary). Input files must be acquired separately from the author or vendor, subject to licensing:

```bash
python reproduce_cpri.py 'OptionChain_CPRI 20-Dec-24_20241023.csv' 'OptionChain_CPRI 20-Dec-24_20241024.csv' 'OptionChain_CPRI 20-Dec-24_20241025.csv'
python quoted_hedges.py 'OptionChain_CPRI 20-Dec-24_20241023.csv' 'OptionChain_CPRI 20-Dec-24_20241025.csv'
python quote_quality_and_iv.py
```

Run these commands in the **repository root**, with all three CSV files there. The scripts do not model synchronized execution, transaction fees, funding or early exercise.

## Market data rights

Original Market Chameleon CSV files are deliberately absent from this public repository. The selected summary is attributed to its original historical-data provider. Further sharing remains subject to any applicable vendor licence or use restrictions.
