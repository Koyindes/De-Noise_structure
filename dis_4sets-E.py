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
    global sets, colors, mp_gap
    
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
        
    fig = plt.figure(figsize=(12, 12), constrained_layout=True)
    # gs = fig.add_gridspec(nrows=10, ncols=5, hspace=0.5)
    gs = fig.add_gridspec(nrows=4, ncols=4, hspace=0.05, wspace=0.05)
    
    count = 0
    for i in range(len(sets)):
        tups = list(combinations(sets, i+1))
        for j, tup in enumerate(tups):
            lx = count % 4
            ly = int(count / 4)
            
            ax = fig.add_subplot(gs[lx, ly])
            
            mps = mp_gap['E'].keys()
            for s in tup:
                another = mp_gap[s].keys()
                mps = [x for x in mps if x in another]
                    
            data = {}
            custom_lines = []
            custom_word = []
            for s in tup:
                gap = [mp_gap[s][mp]-mp_gap['E'][mp] for mp in mps]
                mean = np.mean(gap)
                var = np.var(gap)
                data[mean] = [s, mean, np.sqrt(var)]
                
                sns.distplot(gap, ax=ax, hist=False, kde=True, kde_kws={"color": colors[s]})
                
            data = sorted(data.items(), key=lambda x:x[0])
            intsec_str = r'on $'
            for key, value in data:
                if intsec_str[-1] != '$':
                    intsec_str += ' \cap '
                custom_lines.append(all_custom_lines[value[0]])
                custom_word.append(f'Error({value[0]}, E) ({round(value[1], 2)}, {round(value[2], 2)})')
                intsec_str += '\mathrm{' + value[0] + '}'
            intsec_str += ' \cap \mathrm{E}$'
           
            ax.set_xlim((-5, 5))
            ax.set_ylim((0, 2.0))
            ax.get_yaxis().set_visible(False)
            ax.get_xaxis().set_visible(False)
            
            if ly == 0:
                ax.get_yaxis().set_visible(True)
                ax.get_yaxis().set_ticks(np.arange(0, 2.1, 0.4))
                if lx == 2:
                    ax.set_ylabel('Kernel Density Estimate')
                else:
                    ax.set_ylabel('')
                
            if lx == 3:
                ax.get_xaxis().set_visible(True)
                ax.get_xaxis().set_ticks(np.arange(-4, 5, 2))
                if ly == 2:
                    ax.set_xlabel('Band Gap, eV')
                    
            custom_lines.append(all_custom_lines['empty'])
            custom_word.append(intsec_str)
            ax.legend(custom_lines, custom_word)
            ax.tick_params(labelsize=13)
            count += 1
        
    fig.savefig("4sets_E_dis_v2_new.pdf")
    
def main():
    global sets, colors, mp_gap
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
    
    sets = ['P', 'H', 'S', 'G']
    
    draw()
    
if __name__ == '__main__':
    main()
