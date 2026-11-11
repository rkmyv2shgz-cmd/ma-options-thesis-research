# CPRI selected historical option quotations — thesis input summary

This directory contains a **small, selected-quote summary** of the Market Chameleon historical CPRI chain used in the thesis. It is **not** a downloaded full historical option-chain export.

## Quote summary

CPRI, options expiring **20 December 2024**; prices in US dollars per share.

| Observation date | Underlying spot | $40 put bid / ask | $35 put bid / ask | $40/$35 put vertical midpoint | Quoted side range |
|---|---:|---:|---:|---:|---:|
| 23 Oct 2024 | 41.81 | 7.10 / 8.30 | 5.80 / 6.40 | **1.60** | 0.70–2.50 |
| 24 Oct 2024 | 41.53 | 6.80 / 8.30 | 5.80 / 6.00 | **1.65** | 0.80–2.50 |
| 25 Oct 2024 | 21.25 | 18.60 / 18.90 | 13.70 / 14.00 | **4.90** | 4.60–5.20 |

Also selected for the indicative collar demonstration: the $45 call had a **bid of $6.30 on 23 October** with **zero reported daily trading volume**; its **ask was $0.15 on 25 October**. These are not synchronized transactions.

## Data provenance

- **23–24 October:** selected strike and quote fields read from the author's downloaded Market Chameleon historical option-chain CSV files for CPRI, 20-Dec-2024 maturity. Those full CSV exports are not publicly redistributed here.
- **25 October:** manually transcribed from the author's historical-chain **screenshot**, **not an original CSV export**. Unshown fields are left blank in the summary.
- All figures are historical displayed quotes. Individual legs may be stale or asynchronous, bid–ask sizes and timestamps are not verified, and US equity options are American style.

## Derived calculation

The long $40 put / short $35 put vertical has width $5. Its indicative midpoint is

`[(put40_bid + put40_ask)/2] - [(put35_bid + put35_ask)/2]`.

Its quote-side sale and purchase bounds are `put40_bid - put35_ask` and `put40_ask - put35_bid`. **They are not confidence intervals.** On 25 October the purchase-side value is $5.20, higher than the maximum terminal payoff of $5, illustrating quote asynchronicity/non-executability concerns. The midpoint divided by $5 is **not a verified real-world deal-failure probability**.

The executable research source code is at the repository root: [`reproduce_cpri.py`](../reproduce_cpri.py), [`quoted_hedges.py`](../quoted_hedges.py), and [`quote_quality_and_iv.py`](../quote_quality_and_iv.py). The first two analysis scripts consume the **author's original October 23/24 CSV formats** rather than this compact summary; the 25 October screenshot observations are transcribed into their source code.

See the [spread visualization](../figures/cpri_put_spread.svg).

## Redistribution

This is an attributed, selected and derived *research summary*; it is not represented as a full vendor download. The Market Chameleon source files and screenshot are not reproduced or included. Check market-data licensing terms before further redistribution.
