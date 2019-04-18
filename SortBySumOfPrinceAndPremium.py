import pandas as pd
# import tushare as ts
# import numpy as np
import requests
import time
from datetime import datetime
# import json
import matplotlib.pyplot as plt

exclude_bonds = []
SELECT_RANGE = 30
TOP_RANGE = 18
TODAY = datetime.today().strftime('%Y-%m-%d')
FACTOR = 1    # define the prediction of market. eg. 1 UNKONW, 0.75 WORRY, 1.5 EXCITED

jisiluUrl = "https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t=" + str(time.time())
resp = requests.get(url=jisiluUrl)
data = resp.json()
cbonds=[]
for r in data['rows']:
    cbonds.append(r['cell'])
jdf = pd.DataFrame.from_dict(cbonds)        # jisilu df
jdf.bond_id = jdf.bond_id.astype(str)

#origin raw data
rdf = jdf.loc[(jdf.btype=='C')&( ~jdf.bond_id.isin(exclude_bonds))&(jdf.price!='100.000'), ['bond_id', 'bond_nm', 'increase_rt', 'price', 'sincrease_rt', 'premium_rt', 'adj_scnt', 'ytm_rt',  'rating_cd','year_left', 'curr_iss_amt',  'convert_cd']]
rdf.premium_rt = rdf.premium_rt.apply(lambda s: s.replace('%', ''))
rdf.premium_rt = rdf.premium_rt.astype('float')
rdf.ytm_rt = rdf.ytm_rt.apply(lambda s: s.replace('%', ''))
rdf.ytm_rt = rdf.ytm_rt.astype('float')
rdf.sincrease_rt = rdf.sincrease_rt.apply(lambda s: s if '%' in s else '0.0%')
rdf.sincrease_rt = rdf.sincrease_rt.apply(lambda s: s.replace('%', ''))
rdf.sincrease_rt = rdf.sincrease_rt.astype('float')
rdf.premium_rt = rdf.apply(lambda r: round(r.premium_rt, 2), axis=1)
rdf.ytm_rt = rdf.apply(lambda r: round(r.ytm_rt, 2), axis=1)
rdf.year_left = rdf.year_left.astype('float')
rdf.price = rdf.price.astype('float')

rdf['sum'] = 200 - rdf.price - FACTOR * rdf.premium_rt
rdf.sort_values(by=['sum'], ascending=False, inplace=True)
rdf.reset_index(drop=True, inplace=True)


rdf30_attack = rdf.copy().head(SELECT_RANGE)
rdf30_attack.sort_values(by=['premium_rt'], ascending=True, inplace=True)
rdf18_attack = rdf30_attack.head(TOP_RANGE)
rdf18_attack.loc['TOTAL', 'price'] = rdf18_attack.price.mean()
rdf18_attack.loc['TOTAL', 'premium_rt'] = rdf18_attack.premium_rt.mean()

#top18 rdfs
rdf30_defence = rdf.copy().head(SELECT_RANGE)
rdf30_defence.sort_values(by=['price'], ascending=True, inplace=True)
rdf18_defence = rdf30_defence.head(TOP_RANGE)
rdf18_defence.loc['TOTAL', 'price'] = rdf18_defence.price.mean()
rdf18_defence.loc['TOTAL', 'premium_rt'] = rdf18_defence.premium_rt.mean()

rdf18 = rdf.copy().head(TOP_RANGE)
rdf18.loc['TOTAL', 'price'] = rdf18.price.mean()
rdf18.loc['TOTAL', 'premium_rt'] = rdf18.premium_rt.mean()

replica_rdf = rdf.copy()
replica_rdf.loc['TOTAL', 'price'] = replica_rdf.price.mean()
replica_rdf.loc['TOTAL', 'premium_rt'] = replica_rdf.premium_rt.mean()

with open('existing_bonds.txt') as f:
    exist_bonds = f.readlines()
exist_bonds = set([x.strip() for x in exist_bonds])
exist_df = rdf.loc[rdf.bond_id.isin(exist_bonds), :]
exist_df.loc['TOTAL', 'price'] = exist_df.price.mean()
exist_df.loc['TOTAL', 'premium_rt'] = exist_df.premium_rt.mean()
exist_df.loc['TOTAL','ytm_rt'] = exist_df.ytm_rt.mean()
exist_df.loc['TOTAL','sincrease_rt'] = exist_df.sincrease_rt.mean()

replica_rdf.to_csv('jsl.rlst.csv', encoding='utf-8')
rdf18_attack.to_csv('jsl.attack.18.csv', encoding='utf-8')
rdf18_defence.to_csv('jsl.defence.18.csv', encoding='utf-8')
exist_df.to_csv('jsl.existing.18.csv', encoding='utf-8')
#save to data folder
replica_rdf.to_csv('data/' + TODAY + '.jsl.rlst.csv', encoding='utf-8')
rdf18_attack.to_csv('data/' + TODAY + '.jsl.attack.18.csv', encoding='utf-8')
rdf18_defence.to_csv('data/' + TODAY + '.jsl.defence.18.csv', encoding='utf-8')
exist_df.to_csv('data/' + TODAY + '.jsl.existing.18.csv', encoding='utf-8')

#sell and buy
top18_attack = set(rdf18_attack.bond_id.tolist())
top18_defence = set(rdf18_defence.bond_id.tolist())
top18 = set(rdf18.bond_id.tolist())

# target_bonds = top18_attack
target_bonds = top18_defence
# target_bonds = top18
sell_bonds = exist_bonds - target_bonds
buy_bonds = target_bonds - exist_bonds
sell_df = rdf.loc[rdf.bond_id.isin(sell_bonds), :]
buy_df = rdf.loc[rdf.bond_id.isin(buy_bonds), :]

print 'sell:'
print sell_df
print 'buy:'
print buy_df

special_rdf = rdf.loc[~rdf.convert_cd.str.startswith('1'), ['price', 'premium_rt']]
plt.plot(rdf['price'], rdf['premium_rt'], 'b+')
plt.plot(special_rdf['price'], special_rdf['premium_rt'], 'bx')
plt.plot(exist_df['price'], exist_df['premium_rt'], 'ro')
plt.axis([80, 150, -10, 60])
plt.title(datetime.now().strftime("%Y-%m-%d %I:%M:%S"))
plt.xlabel('price')
plt.ylabel('premium_ratio')
plt.savefig('pic/'+ TODAY + '.png')



