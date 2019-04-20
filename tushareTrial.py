import tushare as ts

stock = ts.get_realtime_quotes('300058')
bond = ts.get_realtime_quotes('123001')

print (float(stock.loc[0, 'bid'])*23.2 > float(bond.loc[0, 'a1_p']) * 1.005) & (float(bond.loc[0, 'a1_v']) > 4.3)

