import pandas as pd
import matplotlib.pyplot as plt
DATE = '2019-04-23'
FULL_DATA_FILE_PATH = './data/'+DATE+'.jsl.rlst.csv'
PARTIAL_FILE_PATH = './data/'+DATE+'.jsl.existing.18.csv'    # only read bond_id from the file

rdf = pd.read_csv(FULL_DATA_FILE_PATH, dtype={'bond_id': object}, encoding='utf-8', index_col=0)
rdf.drop(rdf.tail(1).index, inplace=True)

partial_csv_df = pd.read_csv(PARTIAL_FILE_PATH, dtype={'bond_id': object}, encoding='utf-8', index_col=0)
partial_csv_df.drop(partial_csv_df.tail(1).index, inplace=True)


special_rdf = rdf.loc[~rdf.convert_cd.str.startswith('1'), ['price', 'premium_rt']]
plt.plot(rdf['price'], rdf['premium_rt'], 'b+')
plt.plot(special_rdf['price'], special_rdf['premium_rt'], 'bx')
plt.plot(partial_csv_df['price'], partial_csv_df['premium_rt'], 'ro')
plt.axis([90, 160, -10, 40])
plt.title(DATE + ' 03:40:21')
plt.xlabel('price')
plt.ylabel('premium_ratio')
plt.grid(True)
# plt.show()
# plt.savefig('pic/'+ TODAY + '.png', dpi=300)
plt.savefig('pic/'+ DATE + '.png')
