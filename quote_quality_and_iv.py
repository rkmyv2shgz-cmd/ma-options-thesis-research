"""Historical CPRI contract quote audit using dated 23/24 October 2024 files.
Requires numpy scipy pandas. Does not redistribute vendor files. American equity
options are not European: Black-Scholes inversion/parity calculations here are
only sensitivity diagnostics and *not* no-arbitrage evidence or true IV labels.
"""
from pathlib import Path
from math import exp,log,sqrt
from scipy.stats import norm
from scipy.optimize import brentq
import pandas as pd
import csv

DATA=[('2024-10-23',41.81,58,'OptionChain_CPRI 20-Dec-24_20241023.csv'),
      ('2024-10-24',41.53,57,'OptionChain_CPRI 20-Dec-24_20241024.csv')]
R=.05

def put_bs(S,K,T,s):
 d1=(log(S/K)+(R+.5*s*s)*T)/(s*sqrt(T));d2=d1-s*sqrt(T)
 return K*exp(-R*T)*norm.cdf(-d2)-S*norm.cdf(-d1)

def implied(S,K,T,p):
 lower=max(0.,K*exp(-R*T)-S)
 upper=K*exp(-R*T)
 if p <= lower+1e-8 or p >= upper-1e-8:return None
 return brentq(lambda s:put_bs(S,K,T,s)-p,1e-6,6.,xtol=1e-9)

records=[]
for date,S,days,fn in DATA:
 f=Path(__file__).with_name(fn)
 if not f.exists():f=Path('/mnt/data')/fn
 rows=list(csv.reader(open(f,encoding='utf-8-sig')))[2:]
 for row in rows:
  if len(row)<25:continue
  try:
   K=float(row[16]);pbid=float(row[18]);pask=float(row[20]);cbid=float(row[11]);cask=float(row[13]);pv=int(row[23]);poi=int(row[24])
  except (ValueError,IndexError):continue
  if not all(x>=0 for x in [pbid,pask,cbid,cask]):continue
  T=days/365
  mid=(pbid+pask)/2
  vbid=implied(S,K,T,pbid)
  vask=implied(S,K,T,pask)
  vega_fragile=int(vbid is None or vask is None or (vask-vbid if vbid and vask else 0)>.5)
  # European no-dividend parity: C - P = S - PV(K) (not exact for American options).
  parity=S-K*exp(-R*T)
  residual_mid=((cbid+cask)/2-mid)-parity
  lower=cbid-pask-parity
  upper=cask-pbid-parity
  records.append(dict(date=date,strike=K,days_to_expiry=days,put_bid=pbid,put_ask=pask,
     call_bid=cbid,call_ask=cask,put_volume=pv,put_open_interest=poi,
     put_relative_quoted_spread=((pask-pbid)/mid if mid else None),
     bs_put_bid_iv=vbid,bs_put_ask_iv=vask,bs_iv_interval_width=((vask-vbid) if vbid is not None and vask is not None else None),
     naive_european_parity_mid_residual=residual_mid,
     naive_european_residual_low=lower,naive_european_residual_high=upper,
     parity_zero_inside_quote_interval=lower<=0<=upper,
     numerically_fragile=vega_fragile,invalid_crossed_bidask=int(pask<pbid or cask<cbid)))
df=pd.DataFrame(records)
df.to_csv(Path(__file__).with_name('cpri_quote_quality_diagnostics.csv'),index=False,float_format='%.8f')
for date,g in df.groupby('date'):
 print(date,'n',len(g),'crossed',g.invalid_crossed_bidask.sum(),'fragile IV',g.numerically_fragile.sum(),
       'put volume=0',int((g.put_volume==0).sum()),'parity bracket excludes zero',int((~g.parity_zero_inside_quote_interval).sum()))
 print(g.loc[g.strike.isin([35,40]),['strike','put_bid','put_ask','bs_put_bid_iv','bs_put_ask_iv','put_relative_quoted_spread','naive_european_parity_mid_residual']].to_string(index=False))
