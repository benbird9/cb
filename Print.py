import pandas as pd
import matplotlib.pyplot as plt

FULL_DATA_FILE_PATH = './jsl.rlst.csv'
PARTIAL_FILE_PATH = './jsl.existing.18.csv'    # only read bond_id from the file

rdf = pd.read_csv(FULL_DATA_FILE_PATH, dtype={'bond_id': object}, encoding='utf-8', index_col=0)
rdf.drop(rdf.tail(1).index, inplace=True)

partial_csv_df = pd.read_csv(PARTIAL_FILE_PATH, dtype={'bond_id': object}, encoding='utf-8', index_col=0)
partial_csv_df.drop(partial_csv_df.tail(1).index, inplace=True)
partial_bonds_set = set(partial_csv_df['bond_id'].tolist())
partial_rdf = rdf.loc[rdf.bond_id.isin(partial_bonds_set), :]

print partial_rdf.price.mean()

plt.plot(rdf['price'], rdf['premium_rt'], 'bo')
plt.plot(partial_rdf['price'], partial_rdf['premium_rt'], 'ro')
# plt.axis([80, 150, -10, 60])
plt.show()

