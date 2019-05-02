import pandas as pd
# import tushare as ts
# import numpy as np
import requests
import time
# import json
# import matplotlib.pyplot as plt
exclude_bonds = []
SELECT_RANGE = 30
TOP_RANGE = 18

jisiluUrl = "https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t=" + str(time.time())
resp = requests.get(url=jisiluUrl)
data = resp.json()
cbonds=[]
for r in data['rows']:
    cbonds.append(r['cell'])
jdf = pd.DataFrame.from_dict(cbonds)        # jisilu df
jdf.bond_id = jdf.bond_id.astype(str)


rdf = jdf.loc[(jdf.btype=='C')&( ~jdf.bond_id.isin(exclude_bonds))&(jdf.price!='100.000'), ['bond_id', 'bond_nm', 'increase_rt', 'price', 'sincrease_rt', 'premium_rt', 'adj_scnt', 'ytm_rt',  'rating_cd','pb','year_left',  'curr_iss_amt',  'convert_cd',]]
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
rdf['yield100'] = rdf.apply(lambda r: round((100 - r.price)/r.year_left, 2), axis =1)
rdf['attack'] = rdf.apply(lambda r: round(100 - 2.5*r.premium_rt, 2), axis =1)
rdf['defence'] = rdf.apply(lambda r: round(33.33*r.yield100, 2), axis =1)
# rdf['attack'] = rdf.apply(lambda r: round(100 - 2.5*r.premium_rt, 2), axis =1)
# rdf['defence'] = rdf.apply(lambda r: round(33.33*r.ytm_rt, 2), axis =1)
rdf['sum'] = rdf.attack + rdf.defence
rdf.sort_values(by=['sum'], ascending=False, inplace=True)
rdf.reset_index(drop=True, inplace=True)


rdf30_attack = rdf.copy().head(SELECT_RANGE)
rdf30_attack.sort_values(by=['attack'], ascending=False, inplace=True)
rdf18_attack = rdf30_attack.head(TOP_RANGE)
rdf18_attack.loc['TOTAL', 'price'] = rdf18_attack.price.mean()
rdf18_attack.loc['TOTAL', 'premium_rt'] = rdf18_attack.premium_rt.mean()

rdf30_defence = rdf.copy().head(SELECT_RANGE)
rdf30_defence.sort_values(by=['defence'], ascending=False, inplace=True)
rdf18_defence = rdf30_defence.head(TOP_RANGE)
rdf18_defence.loc['TOTAL', 'price'] = rdf18_defence.price.mean()
rdf18_defence.loc['TOTAL', 'premium_rt'] = rdf18_defence.premium_rt.mean()

rdf18 = rdf.copy().head(TOP_RANGE)
rdf18.loc['TOTAL', 'price'] = rdf18.price.mean()
rdf18.loc['TOTAL', 'premium_rt'] = rdf18.premium_rt.mean()
#output to csv
# rdf.to_csv('jsl.rlst.csv', sep='\t', encoding='utf-8')
# rdf18_attack.to_csv('jsl.attack.18.csv', sep='\t', encoding='utf-8')
# rdf18_defence.to_csv('jsl.defence.18.csv', sep='\t', encoding='utf-8')

replica_rdf = rdf.copy()
replica_rdf.loc['TOTAL', 'price'] = replica_rdf.price.mean()
replica_rdf.loc['TOTAL', 'premium_rt'] = replica_rdf.premium_rt.mean()
replica_rdf.to_csv('jsl.rlst.csv', encoding='utf-8')
rdf18_attack.to_csv('jsl.attack.18.csv', encoding='utf-8')
rdf18_defence.to_csv('jsl.defence.18.csv', encoding='utf-8')

top18_attack = set(rdf18_attack.bond_id.tolist())
top18_defence = set(rdf18_defence.bond_id.tolist())
top18 = set(rdf18.bond_id.tolist())

with open('existing_bonds.txt') as f:
    exist_bonds = f.readlines()
exist_bonds = set([x.strip() for x in exist_bonds])
exist_df = rdf.loc[rdf.bond_id.isin(exist_bonds), :]
exist_df.loc['TOTAL', 'price'] = exist_df.price.mean()
exist_df.loc['TOTAL', 'premium_rt'] = exist_df.premium_rt.mean()
exist_df.loc['TOTAL','ytm_rt'] = exist_df.ytm_rt.mean()
exist_df.loc['TOTAL','sincrease_rt'] = exist_df.sincrease_rt.mean()
exist_df.to_csv('jsl.existing.18.csv', encoding='utf-8')

# target_bonds = top18_attack
# target_bonds = top18_defence
target_bonds = top18
sell_bonds = exist_bonds - target_bonds
buy_bonds = target_bonds - exist_bonds
sell_df = rdf.loc[rdf.bond_id.isin(sell_bonds), :]
buy_df = rdf.loc[rdf.bond_id.isin(buy_bonds), :]

print 'sell:'
print sell_df
print 'buy:'
print buy_df



# rdf.plot()
# plt.show()



