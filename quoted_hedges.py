"""Illustrative two-session CPRI defensive hedges, NOT verified executed trades.
Uses author-downloaded Market Chameleon 23-Oct and 25-Oct 2024 historical
option-chain CSVs, both for the 20-Dec-2024 expiry. The full files are not
redistributed via GitHub. Underlying spot observations come from the archived
Market Chameleon historical-chain screen snapshots (the option CSV excludes spot).
Separate bid and ask legs are not verified synchronized executable quotations.
"""
import argparse
import csv
from pathlib import Path

def read_strike(csv_file, strike):
    with open(csv_file, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    assert rows[1][16] == "Strike Price"
    row = next(row for row in rows[2:] if len(row) > 24 and float(row[16]) == strike)
    assert row[15].strip() == "CPRI 20-Dec-24"
    return {
        "call_bid": float(row[11]), "call_ask": float(row[13]),
        "put_bid": float(row[18]), "put_ask": float(row[20]),
        "call_volume": int(row[9]), "put_volume": int(row[23])
    }

def compute(csv23, csv25):
    entry_put40 = read_strike(csv23, 40)
    entry_call45 = read_strike(csv23, 45)
    exit_put40 = read_strike(csv25, 40)
    exit_call45 = read_strike(csv25, 45)
    spot_entry, spot_exit = 41.81, 21.25  # historical-chain screenshots
    stock = spot_exit - spot_entry
    protective_put = stock + exit_put40["put_bid"] - entry_put40["put_ask"]
    collar = protective_put + entry_call45["call_bid"] - exit_call45["call_ask"]
    assert round(stock, 2) == -20.56
    assert round(protective_put, 2) == -10.26
    assert round(collar, 2) == -4.11
    return {
        "unhedged_stock": stock,
        "protective_put": protective_put,
        "collar": collar,
        "put_entry_ask": entry_put40["put_ask"],
        "put_exit_bid": exit_put40["put_bid"],
        "call_entry_bid": entry_call45["call_bid"],
        "call_exit_ask": exit_call45["call_ask"],
        "call_contract_volume_day23": entry_call45["call_volume"],
        "put_contract_volume_day23": entry_put40["put_volume"]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("oct23_csv", type=Path)
    parser.add_argument("oct25_csv", type=Path)
    args = parser.parse_args()
    print(compute(args.oct23_csv, args.oct25_csv))
    print("WARNING: displayed quote-side scenario, not synchronized executions or realized investor P&L.")
