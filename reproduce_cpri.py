"""Reproduce the CPRI December 2024 put vertical from three author-downloaded Market Chameleon CSV exports.
Inputs are the original historical-chain CSV files for 23, 24 and 25 October 2024.
The raw vendor CSVs are not redistributed through this public repository.
The stock spot values are from the archived historical-chain screen snapshots;
the option-chain CSV itself has no underlying-spot field.
No output is a physical or risk-neutral merger-failure probability.
"""
import argparse
import csv
from pathlib import Path

SPOT_FROM_ARCHIVED_SCREENS = {
    "2024-10-23": 41.81, "2024-10-24": 41.53, "2024-10-25": 21.25
}

def parse_one(path, obs_date):
    with open(path, encoding="utf-8-sig", newline="") as f:
        raw = list(csv.reader(f))
    if len(raw) < 4 or raw[1][16] != "Strike Price" or raw[1][18] != "Bid Price" or raw[1][20] != "Ask Price":
        raise ValueError("Unexpected CSV structure; expected Market Chameleon historical option chain")
    strikes = {float(row[16]): row for row in raw[2:] if len(row) > 24 and row[16]}
    out = {"date": obs_date, "spot": SPOT_FROM_ARCHIVED_SCREENS[obs_date],
           "provenance": "Market Chameleon author-downloaded CSV"}
    for strike in (35, 40):
        row = strikes[strike]
        assert row[15].strip() == "CPRI 20-Dec-24", row[15]
        out[f"p{strike}_bid"] = float(row[18])
        out[f"p{strike}_ask"] = float(row[20])
        out[f"p{strike}_volume"] = int(row[23])
        out[f"p{strike}_open_interest"] = int(row[24])
    return out

def spread(row):
    p40mid = (row["p40_bid"] + row["p40_ask"]) / 2
    p35mid = (row["p35_bid"] + row["p35_ask"]) / 2
    return {
        **row,
        "vertical_mid": round(p40mid - p35mid, 4),
        "quoted_sale_side": round(row["p40_bid"] - row["p35_ask"], 4),
        "quoted_purchase_side": round(row["p40_ask"] - row["p35_bid"], 4),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv23", type=Path)
    parser.add_argument("csv24", type=Path)
    parser.add_argument("csv25", type=Path)
    parser.add_argument("--output", type=Path, default=Path("cpri_vertical_reproduced.csv"))
    args = parser.parse_args()
    observations = [
        parse_one(args.csv23, "2024-10-23"),
        parse_one(args.csv24, "2024-10-24"),
        parse_one(args.csv25, "2024-10-25"),
    ]
    data = [spread(obs) for obs in observations]
    assert [row["vertical_mid"] for row in data] == [1.60, 1.65, 4.90]
    cols = ["date", "spot", "p40_bid", "p40_ask", "p35_bid", "p35_ask",
            "vertical_mid", "quoted_sale_side", "quoted_purchase_side", "provenance"]
    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)
    for row in data:
        print(f'{row["date"]}: midpoint ${row["vertical_mid"]:.2f}; '
              f'quoted sale/purchase sides ${row["quoted_sale_side"]:.2f}–'
              f'${row["quoted_purchase_side"]:.2f}')
    print("Caution: American options, non-synchronized legs; spread divided by $5 is NOT an identified deal-failure probability.")

if __name__ == "__main__":
    main()
