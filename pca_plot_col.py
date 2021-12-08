import json
import sys
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import seaborn as sns

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

def cal(c1, c2):
    x = int(c1, 16)
    y = int(c2, 16)
    res = hex(int((x * 0.6 + y) / 1.6))
    if len(res) == 4:
        return res[2:4]
    else:
        return '0'+res[-1]
        
def get_color(c1, c2):
    return '#' + cal(c1[1:3], c2[1:3]) + cal(c1[3:5], c2[3:5]) + cal(c1[5:7], c2[5:7])
    
def plt_scatter(pca_data, ax2, x, y, label_name):
    global colors
    col = colors[label_name[0]]
    for s in range(1, len(label_name)):
        col = get_color(col, colors[label_name[s]])
    if len(pca_data) != 0:
        print(label_name, col)
        ax2.scatter([n[x] for n in pca_data], [n[y] for n in pca_data], cmap='YlGnBu', marker='.', c=col, s=3, label=label_name)

def single_set_distribution(df_name, pca_total, sort_total, x, y):
    global colors
    
    for sigma in range(3, 4):
        fig = plt.figure(figsize=(8,3.5))
        outer_grid = gs.GridSpec(1, 2)
        
        inner_grid = gs.GridSpecFromSubplotSpec(2, 2,
            subplot_spec=outer_grid[0], wspace=0.0, hspace=0.0, width_ratios=[0.5, 4], height_ratios=[4, 0.5])
        
        ax = plt.Subplot(fig, inner_grid[3])
        ax.set_xlim(-0.02, 1.02)
        ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        ax.get_yaxis().set_visible(False)
        plt_data_x = []
        for name in df_name[0]:
            if len(pca_total[name]) != 0:
                plt_data_x = plt_data_x + [i[x] for i in pca_total[name]]
        sns.distplot(plt_data_x, ax=ax, hist=False, kde_kws={"shade": True, "color": 'gray', 'facecolor': 'gray'})
        fig.add_subplot(ax)
        
        ax1 = plt.Subplot(fig, inner_grid[0])
        ax1.set_ylim(-0.02, 1.02)
        ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        ax1.get_xaxis().set_visible(False)
        plt_data_y = []
        for name in df_name[0]:
            if len(pca_total[name]) != 0:
                plt_data_y = plt_data_y + [i[y] for i in pca_total[name]]
        sns.distplot(plt_data_y, ax=ax1, hist=False, vertical=True, kde_kws={"shade": True, "color": 'gray', 'facecolor': 'gray'})
        fig.add_subplot(ax1)
        
        ax2 = plt.Subplot(fig, inner_grid[1])
        ax2.set_xlim(-0.02, 1.02)
        ax2.set_ylim(-0.02, 1.02)
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)
        
        for key, value in sort_total:
            if key in df_name[0]:
                plt_scatter(pca_total[key], ax2, x, y, key)
                
        ax2.legend(bbox_to_anchor =(0.5, 1.01), loc=8, ncol = 6, columnspacing=0.5, markerscale=8)
        fig.add_subplot(ax2)
        
        inner_grid = gs.GridSpecFromSubplotSpec(2, 2,
                subplot_spec=outer_grid[1], wspace=0.0, hspace=0.0, width_ratios=[0.5, 4], height_ratios=[4, 0.5])
            
        ax = plt.Subplot(fig, inner_grid[3])
        ax.set_xlim(-0.02, 1.02)
        ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        ax.get_yaxis().set_visible(False)
        sns.distplot(plt_data_x, ax=ax, hist=False, kde_kws={"shade": True, "color": 'gray', 'facecolor': 'gray'})
        fig.add_subplot(ax)
        
        ax1 = plt.Subplot(fig, inner_grid[0])
        ax1.set_ylim(-0.02, 1.02)
        ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        ax1.get_xaxis().set_visible(False)
        sns.distplot(plt_data_y, ax=ax1, hist=False, vertical=True, kde_kws={"shade": True, "color": 'gray', 'facecolor': 'gray'})
        fig.add_subplot(ax1)
        
        ax2 = plt.Subplot(fig, inner_grid[1])
        ax2.set_xlim(-0.02, 1.02)
        ax2.set_ylim(-0.02, 1.02)
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)
        
        for key, value in sort_total:
            if key in df_name[0]:
                ellipse_x = np.array([i[x] for i in pca_total[key]])
                ellipse_y = np.array([i[y] for i in pca_total[key]])
                confidence_ellipse(ellipse_x, ellipse_y, ax2, n_std=sigma, 
                        alpha=0.1, label=key, facecolor=colors[key], zorder=0)
        '''
        for j, name in enumerate(df_name[0]):
            ellipse_x = np.array([i[x] for i in pca_total[name]])
            ellipse_y = np.array([i[y] for i in pca_total[name]])
            confidence_ellipse(ellipse_x, ellipse_y, ax2, n_std=sigma, 
                    alpha=0.1, label=name, facecolor=colors[j], zorder=0)
        '''
        ax2.legend(bbox_to_anchor =(0.5, 1.01), loc=8, ncol = 6, columnspacing=0.5, markerscale=8)
        fig.add_subplot(ax2)
        
        fig.subplots_adjust(top=0.890, bottom=0.065, left=0.04, right=0.99, hspace=0.380, wspace=0.110)
        fig.savefig("confidence_ellipse_std={0}_pca({1},{2}).pdf".format(sigma, x, y))
        
def pca_plot(df_name, pca_total, sort_total, x, y):
    fig = plt.figure(figsize=(7, 7))
    outer_grid = gs.GridSpec(2, 2)
    
    for index, df_name_list in enumerate(df_name):
        inner_grid = gs.GridSpecFromSubplotSpec(2, 2,
            subplot_spec=outer_grid[index], wspace=0.0, hspace=0.0, width_ratios=[0.5, 4], height_ratios=[4, 0.5])
        
        ax = plt.Subplot(fig, inner_grid[3])
        ax.set_xlim(-0.02, 1.02)
        ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        ax.get_yaxis().set_visible(False)
        plt_data = []
        for name in df_name_list:
            if len(pca_total[name]) != 0:
                plt_data = plt_data + [i[x] for i in pca_total[name]]
        sns.distplot(plt_data, ax=ax, hist=False, kde_kws={"shade": True, "color": 'gray', 'facecolor': 'gray'})
        fig.add_subplot(ax)
        
        ax1 = plt.Subplot(fig, inner_grid[0])
        ax1.set_ylim(-0.02, 1.02)
        ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
        ax1.get_xaxis().set_visible(False)
        plt_data = []
        for name in df_name_list:
            if len(pca_total[name]) != 0:
                plt_data = plt_data + [i[y] for i in pca_total[name]]
        sns.distplot(plt_data, ax=ax1, hist=False, vertical=True, kde_kws={"shade": True, "color": 'gray', 'facecolor': 'gray'})
        fig.add_subplot(ax1)
        
        ax2 = plt.Subplot(fig, inner_grid[1])
        ax2.set_xlim(-0.02, 1.02)
        ax2.set_ylim(-0.02, 1.02)
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)
        
        for key, value in sort_total:
            if key in df_name_list:
                plt_scatter(pca_total[key], ax2, x, y, key)
                
        if index == 1:
            ax2.legend(bbox_to_anchor =(0.44, 1.01), loc=8, ncol = 6, columnspacing=0.45, handletextpad=0.2, markerscale=8)
        else:
            ax2.legend(bbox_to_anchor =(0.5, 1.01), loc=8, ncol = 6, columnspacing=0.45, handletextpad=0.2, markerscale=8)
        fig.add_subplot(ax2)
        
    fig.subplots_adjust(top=0.945,bottom=0.04,left=0.05,right=0.965,hspace=0.255,wspace=0.15)
    fig.savefig("plot_pca({0},{1}).pdf".format(x, y))

df_name = [['E', 'P', 'S', 'H', 'G'], ['E', 'PS', 'PH', 'PG', 'SH', 'SG', 'HG'], ['E', 'PSH', 'PSG', 'PHG', 'SHG'], ['E', 'PSHG']]
# colors = ['green', 'm', 'orange', 'red', 'blue', 'darkcyan', 'black']
# P: green H:orange S:blue G:red E:m
colors = {'P':'#008000', 'E':'#bf00bf', 'H':'#ffa500', 'G':'#ff0000', 'S':'#0000ff'}

pca_each = {}
with open('../data/pca.json', encoding='utf-8') as f:
    pca_each = json.load(f)
    f.close()

sort_items = sorted(pca_each.items(), key=lambda x: len(x[1]), reverse=True)

for key, value in sort_items:
    print(key, len(value))

for i in range(3):
    for j in range(i+1, 3):
        pca_plot(df_name, pca_each, sort_items, i, j)
        single_set_distribution(df_name, pca_each, sort_items, i, j)

plt.show()

