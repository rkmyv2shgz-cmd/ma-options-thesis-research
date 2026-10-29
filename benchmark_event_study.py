"""CPRI vs S&P 500 October–November 2024, independently reproducible.
CPRI closes: hand-transcribed from author-provided Barchart CPRI option-contract
historical-price screenshots (underlying Price~ column), cross-checked on the
same dates in the $35/$40 put history. Historical prices not redistributed.
S&P 500 closes: Federal Reserve Bank of St Louis FRED SP500 table (source S&P
Dow Jones Indices), https://fred.stlouisfed.org/data/SP500.
This 20-session illustration is not a cross-deal inference test.
"""
from pathlib import Path
import pandas as pd
import numpy as np

VALUES = [
 ('2024-10-21',42.04,5853.98),('2024-10-22',42.06,5851.20),
 ('2024-10-23',41.81,5797.42),('2024-10-24',41.60,5809.86),
 ('2024-10-25',21.26,5808.12),('2024-10-28',21.39,5823.52),
 ('2024-10-29',20.48,5832.92),('2024-10-30',19.46,5813.67),
 ('2024-10-31',19.74,5705.45),('2024-11-01',20.10,5728.80),
 ('2024-11-04',20.14,5712.69),('2024-11-05',20.52,5782.76),
 ('2024-11-06',22.00,5929.04),('2024-11-07',21.99,5973.10),
 ('2024-11-08',20.52,5995.54),('2024-11-11',19.94,6001.35),
 ('2024-11-12',19.39,5983.99),('2024-11-13',19.65,5985.38),
 ('2024-11-14',20.52,5949.17),('2024-11-15',21.00,5870.62),
]
df=pd.DataFrame(VALUES,columns=['date','cpri_close','sp500_close'])
df['cpri_return']=df.cpri_close.pct_change()
df['market_return']=df.sp500_close.pct_change()
df['market_adjusted_return']=df.cpri_return-df.market_return
l=df.loc[df.date=='2024-10-25'].iloc[0]
# This is an *empirical relative rank*, not a causal test: a selected event,
# daily autocorrelation, clustered event risks and a tiny window invalidate
# conventional significance interpretation.
valid=df.dropna(subset=['market_adjusted_return']).copy()
rnk=int((valid.market_adjusted_return<=l.market_adjusted_return).sum())
rank_proportion=rnk/len(valid)
df.to_csv(Path(__file__).with_name('cpri_sp500_event_window.csv'),index=False,float_format='%.9f')
print(f"CPI reaction day CPRI {l.cpri_return:+.6%}, S&P {l.market_return:+.6%}, market-adjusted {l.market_adjusted_return:+.6%}")
print(f"Most-negative rank {rnk}/{len(valid)}; reference-window fraction {rank_proportion:.4f} (descriptive, not a valid predictive p-value)")
print('First 5-session event-window cumulative arithmetic market-adjusted returns:', df.loc[(df.date>='2024-10-25')&(df.date<='2024-10-31'),'market_adjusted_return'].sum())
print('CPRI total Oct 24 to Nov 15 return:',df.iloc[-1].cpri_close/df.loc[df.date=='2024-10-24'].iloc[0].cpri_close-1)
print('S&P 500 corresponding:',df.iloc[-1].sp500_close/df.loc[df.date=='2024-10-24'].iloc[0].sp500_close-1)
assert abs(l.cpri_return-(-.48894))<.0001
assert rnk==1
