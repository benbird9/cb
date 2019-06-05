import pandas as pd
import matplotlib.pyplot as plt
import datetime

csv = pd.read_csv('./data/csi500.csv')
csv.Date = csv.Date.apply(lambda s: datetime.datetime.strptime(s, "%Y/%m/%d").date())

past_3_years_df = csv.loc[csv.Date > datetime.datetime(2016, 5, 17).date(), :]

list = past_3_years_df.Close.tolist()
for i in range(245):
    list.append(3500.0)
print list
list_b = [(lambda x: 1/x)(i) for i in list]
print list_b


print len(list_b)/sum(list_b)
print sum(list)/len(list)