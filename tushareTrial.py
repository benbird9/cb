import tushare as ts
import pandas as pd



def FloatOrZero(value):
    try:
        return float(value)
    except:
        return 0.0
def printGrid():
    stock = ts.get_realtime_quotes('300058')
    bond = ts.get_realtime_quotes('123001')
    df = pd.DataFrame(columns=['b_benefit', 'b_vol', 'b_price','level', 'a_price', 'a_vol', 'a_benefit'])
    stock_price = float(stock.loc[0, 'bid'])*23.2
    for i in range(1, 6):
        bid_price = FloatOrZero(bond.loc[0, 'b'+str(i)+'_p'])
        bid_volume = FloatOrZero(bond.loc[0, 'b'+str(i)+'_v'])*10
        ask_price = FloatOrZero(bond.loc[0, 'a'+str(i)+'_p'])
        ask_volume = FloatOrZero(bond.loc[0, 'a'+str(i)+'_v'])*10
        df.loc[i] = [(stock_price/bid_price -1)*100 ,bid_volume, bid_price, i, ask_price, ask_volume, (stock_price/ask_price -1)*100]
    print df
    print '\n\n'

import time
while True:
    printGrid()
    time.sleep(5)