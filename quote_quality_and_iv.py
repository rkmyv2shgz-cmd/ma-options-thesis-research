"""Contract-level CPRI quote-quality audit of three author-downloaded historical-chain CSV exports.
Does not redistribute vendor CSVs. Black-Scholes inversion and European parity
are sensitivity diagnostics ONLY, not an American option pricing engine or
an executable arbitrage test; abnormal/invalid inversions are reported as such.
"""
from pathlib import Path
from math import exp, log, sqrt
from scipy.stats import norm
from scipy.optimize import brentq
import pandas as pd
import csv

DATA = [
    ("2024-10-23", 41.81, 58, "OptionChain_CPRI 20-Dec-24_20241023.csv"),
    ("2024-10-24", 41.53, 57, "OptionChain_CPRI 20-Dec-24_20241024.csv"),
    ("2024-10-25", 21.25, 56, "OptionChain_CPRI 20-Dec-24_20241025.csv")
]
R = 0.05  # illustrative constant diagnostic rate, NOT a historical yield-curve fit

def put_bs(S, K, T, sigma):
    d1 = (log(S / K) + (R + 0.5 * sigma * sigma) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return K * exp(-R * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def implied(S, K, T, price):
    lower = max(0.0, K * exp(-R * T) - S)
    upper = K * exp(-R * T)
    if price <= lower + 1e-8 or price >= upper - 1e-8:
        return None
    try:
        return brentq(lambda sigma: put_bs(S, K, T, sigma) - price,
                      1e-6, 6.0, xtol=1e-9)
    except ValueError:
        return None

records = []
for date, S, days, name in DATA:
    path = Path(__file__).with_name(name)
    if not path.exists():
        path = Path("/mnt/data") / name
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))[2:]
    for row in rows:
        if len(row) < 25:
            continue
        try:
            K = float(row[16])
            pbid, pask = float(row[18]), float(row[20])
            cbid, cask = float(row[11]), float(row[13])
            pvol, poi = int(row[23]), int(row[24])
        except (ValueError, IndexError):
            continue
        if min(pbid, pask, cbid, cask) < 0:
            continue
        T = days / 365
        mid = (pbid + pask) / 2
        vbid = implied(S, K, T, pbid)
        vask = implied(S, K, T, pask)
        fragile = int(vbid is None or vask is None or (vask - vbid > 0.5))
        # Naive European no-dividend parity is NOT exact for American equity options.
        parity = S - K * exp(-R * T)
        lower = cbid - pask - parity
        upper = cask - pbid - parity
        records.append({
            "date": date, "strike": K, "days_to_expiry": days,
            "put_bid": pbid, "put_ask": pask,
            "call_bid": cbid, "call_ask": cask,
            "put_volume": pvol, "put_open_interest": poi,
            "put_relative_quoted_spread": ((pask - pbid) / mid if mid else None),
            "bs_put_bid_iv": vbid, "bs_put_ask_iv": vask,
            "bs_iv_interval_width": ((vask - vbid) if vbid is not None and vask is not None else None),
            "naive_european_parity_mid_residual": ((cbid + cask) / 2 - mid) - parity,
            "naive_european_residual_low": lower,
            "naive_european_residual_high": upper,
            "parity_zero_inside_quote_interval": lower <= 0 <= upper,
            "numerically_fragile": fragile,
            "invalid_crossed_bidask": int(pask < pbid or cask < cbid)
        })
df = pd.DataFrame(records)
df.to_csv(Path(__file__).with_name("cpri_quote_quality_diagnostics.csv"),
          index=False, float_format="%.8f")
for date, group in df.groupby("date"):
    print(date, "n", len(group), "crossed", int(group.invalid_crossed_bidask.sum()),
          "fragile IV", int(group.numerically_fragile.sum()),
          "put volume=0", int((group.put_volume == 0).sum()),
          "parity bracket excludes zero",
          int((~group.parity_zero_inside_quote_interval).sum()))
    print(group.loc[group.strike.isin([35, 40]),
                    ["strike", "put_bid", "put_ask", "bs_put_bid_iv",
                     "bs_put_ask_iv", "put_relative_quoted_spread",
                     "naive_european_parity_mid_residual"]].to_string(index=False))
