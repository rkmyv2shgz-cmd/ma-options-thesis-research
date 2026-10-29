"""Indicative two-session CPRI defensive hedges, NOT executed trades.
Source A: Market Chameleon 23-Oct-2024 downloaded option-chain CSV for 20-Dec-2024 expiry.
Source B: Market Chameleon 25-Oct-2024 screenshot manually read by the author.
The stock prices are the historical-chain displayed 'Spot Price' figures on these dates.
All open/exit legs are assumed to transact at displayed bid/ask quote sides, which
is not verifiable from a non-synchronized snapshot. No cash dividends, fees,
financing or American early exercise over the 2 sessions are included.
"""
from pathlib import Path
import csv, argparse

def read_strike(csv_file,k):
    with open(csv_file,encoding='utf-8-sig',newline='') as f:
        rows=list(csv.reader(f))
    assert rows[1][16]=='Strike Price'
    r=next(r for r in rows[2:] if len(r)>23 and float(r[16])==k)
    assert r[15]=='CPRI 20-Dec-24'
    return {'call_bid':float(r[11]), 'call_ask':float(r[13]),
            'put_bid':float(r[18]), 'put_ask':float(r[20]),
            'call_volume':int(r[9]), 'put_volume':int(r[23])}

def compute(csv23):
    day23_p40=read_strike(csv23,40)
    day23_c45=read_strike(csv23,45)
    S0,S1=41.81,21.25
    # 25 October 2024 source: manually transcribed screenshot, not CSV.
    put40_exit_bid=18.60
    call45_exit_ask=0.15
    stock=S1-S0
    longput=stock+(put40_exit_bid-day23_p40['put_ask'])
    collar=longput+(day23_c45['call_bid']-call45_exit_ask)
    assert round(stock,2)==-20.56
    assert round(longput,2)==-10.26
    assert round(collar,2)==-4.11
    return {'unhedged_stock':stock,'protective_put':longput,'collar':collar,
            'put_open_ask':day23_p40['put_ask'],
            'call_open_bid':day23_c45['call_bid'],
            'call_contract_volume_day23':day23_c45['call_volume'],
            'put_contract_volume_day23':day23_p40['put_volume']}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('oct23_csv',type=Path)
    a=parser.parse_args()
    print(compute(a.oct23_csv))
    print('WARNING: indicative quoted-side values; not synchronized executions or realized P&L.')
