import pandas as pd
import matplotlib.pyplot as plt

csv = pd.read_csv('./data/csi500.csv')
csv.Close.min()
plt.plot(csv.Date, csv.Close, 'ro')
plt.show()