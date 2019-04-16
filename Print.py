import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime

p_rdf = pd.read_csv('jsl.rlst.csv', encoding='utf-8')
p_exist_df = pd.read_csv('jsl.defence.18.csv', encoding='utf-8')
plt.plot(p_rdf['price'], p_rdf['premium_rt'], 'bo')
plt.plot(p_exist_df['price'], p_exist_df['premium_rt'], 'ro')
plt.axis([80, 150, -10, 60])
# plt.savefig('pic/'+ datetime.today().strftime('%Y-%m-%d') + '.png')
plt.show()

