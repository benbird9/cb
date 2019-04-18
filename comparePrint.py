import pandas as pd
import matplotlib.pyplot as plt

FROM_FILE_PATH = './data/2019-04-17.jsl.existing.18.csv'
TO_FILE_PATH = './data/2019-04-18.jsl.existing.18.csv'    

from_rdf = pd.read_csv(FROM_FILE_PATH, dtype={'bond_id': object}, encoding='utf-8', index_col=0)
from_rdf.drop(from_rdf.tail(1).index, inplace=True)

to_rdf = pd.read_csv(TO_FILE_PATH, dtype={'bond_id': object}, encoding='utf-8', index_col=0)
to_rdf.drop(to_rdf.tail(1).index, inplace=True)

plt.figure(1)
plt.plot(from_rdf['price'], from_rdf['premium_rt'], 'bo')
plt.plot(to_rdf['price'], to_rdf['premium_rt'], 'ro')
plt.axis([80, 150, -10, 60])
plt.show()
