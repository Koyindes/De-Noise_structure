import pandas as pd
import numpy as np
from upsetplot import UpSet
from matplotlib import pyplot as plt
from upsetplot import plot

miindex = pd.MultiIndex.from_product([[True, False], [True, False], [True, False], [True, False], [True, False]],
        names=['P','H','S','G', 'E'])

micolumns = pd.MultiIndex.from_product([['mp_id']])
     
sets = ["P", "H", "S", "G", "E"]
nsets = len(sets)

df = {}
for set in sets:
    df[set] = pd.read_csv("../data/5set/"+set+".csv")
    
all_mp_id = []
for set in sets:
    for mp_id in df[set]["mp_id"].values:
        if [mp_id] not in all_mp_id:
            all_mp_id.append([mp_id])

nmp = len(all_mp_id)
print(nmp)

for i in range(nmp):
    for set in sets:
        if all_mp_id[i][0] in df[set]["mp_id"].values:
            all_mp_id[i].append(True)
        else:
            all_mp_id[i].append(False)
            
count = np.zeros(len(miindex) * len(micolumns))

for i in range(nmp):
    x = 0
    for j in range(1, nsets+1):
        if all_mp_id[i][j] == False:
            x += 2 ** (5 - j)
    if x == 24:
        print(i, all_mp_id[i][0], x)
    count[x] += 1

miseries = pd.Series(count, index=miindex).sort_index()

print(miseries)

fig = plot(miseries, show_counts=True)
plt.show()


