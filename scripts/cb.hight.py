import tushare as ts

print('bond\thigh\tlow')
with open('../trade/cb.txt') as f:
    for bond in f:
        try:
            df = ts.get_hist_data(bond.strip(), ktype='M',pause=5)
            high = df.high.max()
            low = df.low.min()
            print(bond.strip() + '\t' + str(high) +'\t' + str(low))
        except:
            continue
