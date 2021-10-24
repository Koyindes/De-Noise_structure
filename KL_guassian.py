import json
import sys
import random
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import seaborn as sns

def get_KL(p, q):
    P, Q = [], []
    for i in range(len(p)):
        P.append(p[i] / len(p))
        Q.append(q[i] / len(p))
    s = [0, 0]
    for i in range(len(p)):
        for j in range(len(p[0])):
            px = P[i][j]
            qx = Q[i][j]
            s[0] += px * np.log(px / qx)
            s[1] += qx * np.log(qx / px)
    return s
            
def noise(x, size, sigma):
    volume = np.zeros(size, dtype=float)
    if x < 1:
        xi = int(x*size)
    else:
        xi = size-1
    volume[xi] = 1
    s = 0
    for i in range(size):
        pow_sum = ((i-xi)/size)**2
        volume[i] += np.exp(-1*pow_sum/(2*sigma**2))
        s += volume[i]
    volume /= s
    return volume

df_name = ['P', 'S', 'H', 'G', 'E']
colors = ['green', 'orange', 'red', 'blue', 'gray', 'purple']

pca_each = {}
with open('../data/megnet96.json', encoding='utf-8') as f:
    pca_each = json.load(f)
    f.close()
    
pca_full_dict = {}
for x in df_name:
    full = []
    for key, value in pca_each.items():
        if x in key:
            full.extend(value)
    pca_full_dict[x] = full
    # print(x, ':', len(full))
pca_full_dict['E'] = pca_each['E']

for size in range(10, 11):
    dim_dic = {}
    for i in range(len(pca_full_dict['P'][0])):
        dic = {}
        for name in df_name:
            p = np.zeros(size, dtype=float)
            for j in range(len(pca_full_dict[name])):
                vol = noise(pca_full_dict[name][j][i], size, np.exp(-size/3))
                for k in range(size):
                    p[k] += vol[k]
            p /= len(pca_full_dict[name])
            dic[name] = p
        dim_dic[i] = dic
    
    p_last = {}
    for name in df_name:
        p_set = []
        for i in range(len(dim_dic)):
            p_set.append(dim_dic[i][name])
        p_last[name] = p_set
    # print(p_last)
    
    KL_E_other = np.zeros((3, len(df_name)-1), dtype=float)
    for i, name in enumerate(df_name):
        if name == 'E':
            continue
        p = p_last['E']
        q = p_last[name]
        KL_E_other[0][i], KL_E_other[1][i] = get_KL(p, q)
    
    KL_one_others = np.zeros((3, len(df_name)-1), dtype=float)
    for i, name in enumerate(df_name):
        if name == 'E':
            continue
        p = p_last[name]
        count = 0
        q = []
        for j in range(len(p)):
            q.append(np.zeros(len(p[0])))
        for q_name in df_name:
            if q_name == 'E' or q_name == name:
                continue
            for j in range(len(p)):
                q[j] += p_last[q_name][j] * len(pca_full_dict[q_name])
            count += len(pca_full_dict[q_name])
        for j in range(len(p)):
            q[j] /= count
        KL_one_others[0][i], KL_one_others[1][i] = get_KL(p, q)
        
    for i in range(len(df_name)-1):
        KL_E_other[2] = (KL_E_other[0] + KL_E_other[1])/2.0
        KL_one_others[2] = (KL_one_others[0] + KL_one_others[1])/2.0
        
    print('E-P', 'E-S', 'E-H', 'E-G')
    print(KL_E_other)
    print('P-SHG', 'S-PHG', 'H-PSG', 'G-PSH')
    print(KL_one_others)
# plt.show()

