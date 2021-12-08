import json
import sys
import random
import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull
import copy

df_name = [['E', 'P', 'S', 'H', 'G'], ['E', 'PS', 'PH', 'PG', 'SH', 'SG', 'HG'], ['E', 'PSH', 'PSG', 'PHG', 'SHG'], ['E', 'PSHG']]
colors = ['green', 'm', 'orange', 'red', 'blue', 'darkcyan', 'black']

pca_each = {}
with open('../data/megnet96.json', encoding='utf-8') as f:
    pca_each = json.load(f)
    f.close()
print(pca_each['E'][0])
E = np.array(pca_each['E'])

'''
hull = ConvexHull(E)
sim = hull.simplices
total = 0
count = 0
new_hull = copy.deepcopy(hull)
for key, value in pca_each.items():
    if 'H' in key:
        for i, point in enumerate(value):
            print(key, total+i)
            p = np.array(point)
            new_hull.add_points(p)
            new_sim = new_hull.simplices
            if not (sim == new_sim).all():
                count += 1
                new_hull = copy.deepcopy(hull)
        total += len(value)

print('total: ', total)
print(count, 'points are not in hull.')
'''
