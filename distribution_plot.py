import sys
import pandas as pd
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import matplotlib.transforms as transforms
from matplotlib.lines import Line2D
from scipy.stats import norm
import seaborn as sns
import matplotlib.font_manager

def draw():
    global sets, df, colors, mp_gap
    
    font = {'family': 'Arial'}
    matplotlib.rc('font', **font)
    
    plt.rcParams['mathtext.fontset'] = 'custom'
    plt.rcParams['mathtext.it'] = 'Arial:italic'
    plt.rcParams['mathtext.rm'] = 'Arial'
    plt.rcParams['pdf.fonttype'] = 42
    
    all_custom_lines = {}
    for s in sets:
        all_custom_lines[s] = Line2D([0], [0], color=colors[s], lw = 2)
    all_custom_lines["empty"] = Line2D([0], [0], lw = 0)
        
    fig = plt.figure(figsize=(13, 16), constrained_layout=True)
    # gs = fig.add_gridspec(nrows=10, ncols=5, hspace=0.5)
    gs = fig.add_gridspec(nrows=6, ncols=5, hspace=0.05, wspace=0.05)
    
    data = {}
    custom_lines = []
    custom_word = []
    ax = fig.add_subplot(gs[0, 0])
    for s in sets:
        gap = []
        for key, value in mp_gap[s].items():
            p = True
            for another in sets:
                if s == another:
                    continue
                if key in mp_gap[another].keys():
                    p = False
                    break
            if p:
                gap.append(value)
        mean = np.mean(gap)
        var = np.var(gap)
        data[mean] = [s, mean, np.sqrt(var)]
        
        sns.distplot(gap, ax=ax, hist=False, kde_kws={"color": colors[s]})
        
    data = sorted(data.items(), key=lambda x:x[0])
    
    for key, value in data:
        custom_lines.append(all_custom_lines[value[0]])
        custom_word.append(f'{value[0]} Only ({round(value[1], 2)}, {round(value[2], 2)})')
    
    ax.set_xlim((0, 18))
    ax.set_ylim((0, 1.5))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(True)
    ax.set_yticks(np.arange(0, 1.6, 0.3))
    ax.set_ylabel('')
    
    ax.legend(custom_lines, custom_word)
    ax.tick_params(labelsize=13)
        
        
    data = {}
    custom_lines = []
    custom_word = []
    ax = fig.add_subplot(gs[0, 1])
    for s in sets:
        gap = list(mp_gap[s].values())
        mean = np.mean(gap)
        var = np.var(gap)
        data[mean] = [s, mean, np.sqrt(var)]
        
        sns.distplot(gap, ax=ax, hist=False, kde_kws={"color": colors[s]})
        
    data = sorted(data.items(), key=lambda x:x[0])
    
    for key, value in data:
        custom_lines.append(all_custom_lines[value[0]])
        custom_word.append(f'{value[0]} All ({round(value[1], 2)}, {round(value[2], 2)})')
    
    ax.set_xlim((0, 18))
    ax.set_ylim((0, 1.5))
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)
    
    ax.legend(custom_lines, custom_word)
    ax.tick_params(labelsize=13)
    
    l = [1, 3, 5, 0]
    for i in range(len(sets)):
        tups = list(combinations(sets, i+2))
        for j, tup in enumerate(tups):
            lx = l[i] + 1 if j >= 5 else l[i] + 0
            ly = 0
            if i == 0 or i == 1 or i == 2:
                ly = j % 5
            elif i == 3:
                ly = 2
            
            ax = fig.add_subplot(gs[lx, ly])
            
            mps = mp_gap[tup[0]].keys()
            for k, s in enumerate(tup):
                if k == 0:
                    continue
                else:
                    another = mp_gap[s].keys()
                    mps = [x for x in mps if x in another]
                    
            data = {}
            custom_lines = []
            custom_word = []
            for s in tup:
                gap = [mp_gap[s][mp] for mp in mps]
                mean = np.mean(gap)
                var = np.var(gap)
                data[mean] = [s, mean, np.sqrt(var)]
                
                sns.distplot(gap, ax=ax, hist=False, kde_kws={"color": colors[s]})
                
            data = sorted(data.items(), key=lambda x:x[0])
            intsec_str = r'on $'
            for key, value in data:
                if intsec_str[-1] != '$':
                    intsec_str += ' \cap '
                custom_lines.append(all_custom_lines[value[0]])
                custom_word.append(f'{value[0]} ({round(value[1], 2)}, {round(value[2], 2)})')
                intsec_str += '\mathrm{' + value[0] + '}'
            intsec_str += '$'
           
            ax.set_xlim((0, 18))
            ax.set_ylim((0, 1.5))
            ax.get_yaxis().set_visible(False)
            ax.get_xaxis().set_visible(False)
            
            if ly % 5 == 0:
                ax.get_yaxis().set_visible(True)
                ax.get_yaxis().set_ticks(np.arange(0, 1.6, 0.3))
                if lx == 2:
                    ax.set_ylabel('Kernel Density Estimate')
                else:
                    ax.set_ylabel('')
                
            if lx == 5:
                ax.get_xaxis().set_visible(True)
                ax.get_xaxis().set_ticks(np.arange(0, 16, 3))
                if ly == 2:
                    ax.set_xlabel('Band Gap, eV')
                    
            custom_lines.append(all_custom_lines['empty'])
            custom_word.append(intsec_str)
            ax.legend(custom_lines, custom_word)
            ax.tick_params(labelsize=13)
        
    fig.savefig("distribution_v9.pdf")
    
def main():
    global sets, df, colors, mp_gap
    sets = ['P', 'H', 'S', 'G', 'E']
    colors = {'P':'#008000', 'E':'#bf00bf', 'H':'#ffa500', 'G':'#ff0000', 'S':'#0000ff'}
    
    df = {}
    mp_gap = {}
    for s in sets:
        df[s] = pd.read_csv('../data/5set/'+s+'.csv')
        mp_gap[s] = {}
        mp_id = df[s]['mp_id'].values
        gap = df[s]['gap'].values
        for i in range(len(mp_id)):
            mp_gap[s][mp_id[i]] = gap[i]
    
    draw()
    
if __name__ == '__main__':
    main()
