"""Reproduce the CPRI put-vertical table from user-supplied Market Chameleon CSVs.

The October 25 observation is an explicitly labeled screen-transcription, NOT a CSV row.
No output is a physical or risk-neutral merger-failure probability.
"""
import argparse
import csv
import pathlib

SAVED_SCREEN = {"date":"2024-10-25", "spot":21.25,
                "p40_bid":18.60,"p40_ask":18.90,"p35_bid":13.70,"p35_ask":14.00}

def parse_one(path, obs_date, spot_from_screen):
    with open(path, encoding="utf-8-sig", newline="") as f:
        raw=list(csv.reader(f))
    if len(raw)<4 or raw[1][16]!="Strike Price" or raw[1][18]!="Bid Price" or raw[1][20]!="Ask Price":
        raise ValueError("Unexpected CSV structure; check exported option chain")
    strikes={float(r[16]):r for r in raw[2:] if len(r)>24 and r[16]}
    v={"date":obs_date,"spot":spot_from_screen,"provenance":"Market Chameleon CSV"}
    for k in (35,40):
        r=strikes[k]
        assert r[15].strip()=="CPRI 20-Dec-24",r[15]
        v[f'p{k}_bid']=float(r[18]);v[f'p{k}_ask']=float(r[20])
        v[f'p{k}_volume']=int(r[23]);v[f'p{k}_open_interest']=int(r[24])
    return v

def spread(row):
    p40mid=(row['p40_bid']+row['p40_ask'])/2
    p35mid=(row['p35_bid']+row['p35_ask'])/2
    return {
        **row,'vertical_mid':round(p40mid-p35mid,4),
        'quoted_sale_side':round(row['p40_bid']-row['p35_ask'],4),
        'quoted_purchase_side':round(row['p40_ask']-row['p35_bid'],4),
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('csv23', type=pathlib.Path)
    parser.add_argument('csv24', type=pathlib.Path)
    parser.add_argument('--output',type=pathlib.Path,default=pathlib.Path('cpri_vertical_reproduced.csv'))
    args=parser.parse_args()
    data=[parse_one(args.csv23,'2024-10-23',41.81),parse_one(args.csv24,'2024-10-24',41.53),{**SAVED_SCREEN,'provenance':'Manual screenshot transcription'}]
    output=[spread(d) for d in data]
    assert [x['vertical_mid'] for x in output]==[1.6,1.65,4.9]
    assert output[0]['quoted_sale_side']==.7 and output[1]['quoted_sale_side']==.8
    cols=['date','spot','p40_bid','p40_ask','p35_bid','p35_ask','vertical_mid','quoted_sale_side','quoted_purchase_side','provenance']
    with open(args.output,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(output)
    for d in output:
        print(f"{d['date']} mid=${d['vertical_mid']:.2f}, bid/ask quote-side ${d['quoted_sale_side']:.2f}–${d['quoted_purchase_side']:.2f}, {d['provenance']}")
    print('Warning: no 25-Oct CSV; US equity options are American-style; spread normalized by $5 is NOT an identified completion/failure probability.')

if __name__=='__main__':main()
