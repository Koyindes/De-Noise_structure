import numpy as np
import matplotlib.pyplot as plt
import json
from math import log

def KL_divergence(p, q):
    kl = []
    for dim in range(3):
        P = [x[dim] for x in p]
        Q = [x[dim] for x in q]
        
        P_count = np.zeros(101)
        for x in P:
            P_count[int(x/0.01)] += 1
        P_count = P_count.tolist()
        
        Q_count = np.zeros(101)
        for x in Q:
            Q_count[int(x/0.01)] += 1
        Q_count = Q_count.tolist()
            
        s = 0
        for i in range(len(Q_count)):
            px = P_count[i] / sum(P_count)
            qx = Q_count[i] / sum(Q_count)
            if px != 0 and qx != 0:
                s += px * log(px / qx)
        kl.append(s)
    return kl

def KL_3d(p, q):
    kl = 0
    arr_size = 11
    p_distr = np.zeros((arr_size, arr_size, arr_size))
    q_distr = np.zeros((arr_size, arr_size, arr_size))
    arr_size -= 1
    for p_item in p:
        p_distr[(round(p_item[0]*arr_size))][(round(p_item[1]*arr_size))][(round(p_item[2]*arr_size))] += 1
    for q_item in q:
        q_distr[(round(q_item[0]*arr_size))][(round(q_item[1]*arr_size))][(round(q_item[2]*arr_size))] += 1
    arr_size += 1
    for i in range(arr_size):
        for j in range(arr_size):
            for k in range(arr_size):
                px = p_distr[i][j][k] / np.sum(p_distr)
                qx = q_distr[i][j][k] / np.sum(q_distr)
                if px != 0 and qx != 0:
                    kl += px * log(px / qx)
    return kl

def KL_3d_fast(p, q, arr_size):
    kl = 0
    p_dict = {}
    q_dict = {}
    arr_size -= 1
    for p_item in p:
        i = round(p_item[1]*arr_size)
        j = round(p_item[2]*arr_size)
        k = round(p_item[3]*arr_size)
        if (i, j, k) in p_dict.keys():
            p_dict[(i, j, k)] += 1
        else:
            p_dict[(i, j, k)] = 1
    
    for q_item in q:
        i = round(q_item[1]*arr_size)
        j = round(q_item[2]*arr_size)
        k = round(q_item[3]*arr_size)
        if (i, j, k) in q_dict.keys():
            q_dict[(i, j, k)] += 1
        else:
            q_dict[(i, j, k)] = 1
    sum_p = 0
    sum_q = 0
    for key in p_dict.keys():
        sum_p += p_dict[key]
    for key in q_dict.keys():
        sum_q += q_dict[key]
    
    for key in p_dict.keys():
        px = p_dict[key] / sum_p
        if key in q_dict.keys():
            qx = q_dict[key] / sum_q
        else:
            qx = 0

        if px != 0 and qx != 0:
            kl += px * log(px / qx)
        else:
            kl = -1
            break
    return kl

def KL_fast(p, q, arr_size):
    kl = 0
    p_dict = {}
    q_dict = {}
    arr_size -= 1
    for p_item in p:
        i = round(p_item[2]*arr_size)
        if i in p_dict.keys():
            p_dict[i] += 1
        else:
            p_dict[i] = 1
    
    for q_item in q:
        i = round(q_item[2]*arr_size)
        if i in q_dict.keys():
            q_dict[i] += 1
        else:
            q_dict[i] = 1
    sum_p = 0
    sum_q = 0
    for key in p_dict.keys():
        sum_p += p_dict[key]
    for key in q_dict.keys():
        sum_q += q_dict[key]
    
    for key in p_dict.keys():
        px = p_dict[key] / sum_p
        if key in q_dict.keys():
            qx = q_dict[key] / sum_q
        else:
            qx = 0

        if px != 0 and qx != 0:
            kl += px * log(px / qx)
        else:
            kl = -1
            break
    return kl
    
df_name = [['P', 'S', 'H', 'G'], ['PS', 'PH', 'PG', 'SH',	 'SG', 'HG'], ['PSH', 'PSG', 'PHG', 'SHG'], ['PSHG']]
col_name = {'P': 'pbe', 'S': 'scan', 'H': 'hse', 'G': 'gllb-sc'}

pca_dict = {}

with open('../data/pca.json', encoding='utf-8') as f:
    pca_dict = json.load(f)
    f.close()

pca_full_dict = {}
for x in df_name[0]:
    full = []
    for key, value in pca_dict.items():
        if x in key:
            full.extend(value)
    pca_full_dict[x] = full
    print(x, ':', len(full))
pca_full_dict['E'] = pca_dict['E']

col = ['P-SHG', 'S-PHG', 'H-PSG', 'G-PSH']
col_e = ['E-P', 'E-S', 'E-H', 'E-G']
# row = [' pca_0 ', ' pca_1 ', ' pca_2 ']

max_rows = 10
max_kl = np.zeros(4)
max_kl_e = np.zeros(4)

print(pca_dict.keys())

value = np.zeros((max_rows, 4))
for i, left in enumerate(df_name[0]):
    p = pca_full_dict[left]
    print(left, len(p))
    q = []
    for key in pca_full_dict.keys():
        if left != key and key != 'E':
            q.extend(pca_full_dict[key])
    print(len(p), len(q))
    # value[0][i], value[1][i], value[2][i] = KL_divergence(p, q)
    # value[0][i] = KL_3d(p, q)

    for row_idx in range(max_rows-2):
        arr_size = row_idx + 1
        # value[row_idx][i] = KL_3d_fast(p, q, arr_size)
        value[row_idx][i] = KL_fast(p, q, arr_size)
        max_kl[i] = max(max_kl[i], value[row_idx][i])
    # value[-2][i] = KL_3d_fast(p, q, 1001)
    # value[-1][i] = KL_3d_fast(p, q, 10001)
    value[-2][i] = KL_fast(p, q, 1001)
    value[-1][i] = KL_fast(p, q, 10001)
# print(value)
print(max_kl)

value_e = np.zeros((max_rows, 4))
for i, right in enumerate(df_name[0]):
    p = pca_full_dict['E']
    q = []
    for key in pca_full_dict.keys():
        if right in key:
            q.extend(pca_full_dict[key])
    print(right, len(q))
    # value[0][i], value[1][i], value[2][i] = KL_divergence(p, q)
    # value[0][i] = KL_3d(p, q)
    
    for row_idx in range(max_rows-2):
        arr_size = row_idx + 1
        # value_e[row_idx][i] = KL_3d_fast(p, q, arr_size)
        value_e[row_idx][i] = KL_fast(p, q, arr_size)
        max_kl_e[i] = max(max_kl_e[i], value_e[row_idx][i])
    # value_e[-2][i] = KL_3d_fast(p, q, 1001)
    # value_e[-1][i] = KL_3d_fast(p, q, 10001)
    value_e[-2][i] = KL_fast(p, q, 1001)
    value_e[-1][i] = KL_fast(p, q, 10001)
print(max_kl_e)

colors = ['green', 'orange', 'red', 'blue', 'gray', 'purple']

print(value)
print('~~~~~~~~~~~~~~~~~~~')
print(value_e)
fig = plt.figure(figsize=(12,8))
for i in range(len(df_name[0])):
    y = [a[i] for a in value]
    ax = plt.plot(range(1, max_rows+1), y, marker='.', c=colors[i], label=col[i])
plt.subplots_adjust(top=0.85,bottom=0.065,left=0.095,right=0.995,hspace=0.2,wspace=0.2)
plt.tick_params(labelsize=30)
plt.legend(bbox_to_anchor =(0.5, 1.01), loc=8, ncol=4, handlelength=1, columnspacing=0.6, fontsize = 30)

fig = plt.figure(figsize=(12,8))
for i in range(len(df_name[0])):
    y = [a[i] for a in value_e]
    ax = plt.plot(range(1, max_rows+1), y, marker='.', c=colors[i], label=col_e[i])
plt.subplots_adjust(top=0.85,bottom=0.065,left=0.12,right=0.995,hspace=0.2,wspace=0.2)
plt.tick_params(labelsize=30)
plt.legend(bbox_to_anchor =(0.5, 1.01), loc=8, ncol=4, fontsize = 30)

# plt.figure(figsize=(12,6))
# tab = plt.table(cellText = value, 
#               colLabels = col, 
#               rowLabels = row,
#               loc = 'center', 
#               cellLoc = 'center',
#               rowLoc = 'center')
# tab.auto_set_font_size(False)
# tab.set_fontsize(10)
# # tab.scale(1,1.5) 
# plt.subplots_adjust(bottom=0.040, right=0.995, left=0.055, top=1.000)
# plt.axis('off')
plt.show()
