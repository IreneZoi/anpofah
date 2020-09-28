import matplotlib.pyplot as plt
from matplotlib import colors
import os
import numpy as np

import anpofah.util.data_preprocessing as dpr


def subplots_rows_cols(n):
    ''' get number of subplot rows and columns needed to plot n histograms in one figure '''
    return int(np.round(np.sqrt(n))), int(np.ceil(np.sqrt(n)))


def plot_hist(data, bins=100, xlabel='x', ylabel='num frac', title='histogram', plot_name='plot', fig_dir=None, legend=[], ylogscale=True, normed=True, ylim=None, legend_loc='best', xlim=None):
    fig = plt.figure(figsize=(6, 4))
    plot_hist_on_axis(plt.gca(), data, bins=bins, xlabel=xlabel, ylabel=ylabel, title=title, legend=legend, ylogscale=ylogscale, normed=normed, ylim=ylim, xlim=xlim)
    if legend:
        plt.legend(loc=legend_loc)
    plt.tight_layout()
    if fig_dir is not None:
        fig.savefig(os.path.join(fig_dir, plot_name + '.pdf'))
    else:
        plt.show();
    plt.close(fig)


def plot_multihist(data, bins=100, suptitle='histograms', titles=[], plot_name='histograms', fig_dir=None):
    ''' plot len(data) histograms on same figure 
        data = list of features to plot (each element is flattened before plotting)
    '''
    rows_n, cols_n = subplots_rows_cols(len(data))
    fig, axs = plt.subplots(nrows=rows_n,ncols=cols_n, figsize=(9,9))
    for ax, dat, title in zip(axs.flat, data, titles):
        plot_hist_on_axis(ax, dat.flatten(), bins=bins, title=title)
    [a.axis('off') for a in axs.flat[len(data):]] # turn off unused subplots
    plt.suptitle(suptitle)
    plt.tight_layout(rect=(0, 0, 1, 0.95))
    if fig_dir is not None:
        fig.savefig(os.path.join(fig_dir, plot_name + '.pdf'))
    else:
        plt.show();
    plt.close(fig)


def plot_hist_on_axis(ax, data, bins, xlabel='', ylabel='', title='histogram', legend=[], ylogscale=True, normed=True, ylim=None, xlim=None):
    if ylogscale:
        ax.set_yscale('log', nonposy='clip')
    counts, edges, _ = ax.hist(data, bins=bins, normed=normed, histtype='step', label=legend)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    if ylim:
        ax.set_ylim(ylim)
    if xlim:
        ax.set_xlim(xlim)


def plot_hist_2d( x, y, xlabel='x', ylabel='num frac', title='histogram', plot_name='hist2d', fig_dir=None, legend=[],ylogscale=True, normed=True, ylim=None, legend_loc='best', xlim=None, clip_outlier=False):
    
    if clip_outlier:
        idx = dpr.is_outlier_percentile(x) | dpr.is_outlier_percentile(y)
        x = x[~idx]
        y = y[~idx]

    fig = plt.figure()
    ax = plt.gca()
    im = plot_hist_2d_on_axis( ax, x, y, xlabel, ylabel, title )
    fig.colorbar(im[3])
    plt.tight_layout()
    if fig_dir:
        plt.savefig(os.path.join(fig_dir,plot_name+'.png'))
    plt.show()
    plt.close(fig)
    return ax
    
    
def plot_hist_2d_on_axis( ax, x, y, xlabel, ylabel, title ):
    im = ax.hist2d(x, y, bins=100, norm=colors.LogNorm())
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    return im


def plot_bg_vs_sig(data, bins=100, xlabel='x', ylabel='num frac', title='histogram', plot_name='plot', fig_dir=None, legend=[], ylogscale=True, normed=True, legend_loc='best', clip_outlier=False):
    '''
    plots feature distribution treating first data-array as backround and rest of arrays as signal
    :param data: list/array of N elements where first element is assumed to be background and elements 2..N-1 assumed to be signal. all elements = array of length M
    '''
    fig = plt.figure(figsize=(6, 4))
    alpha = 0.4
    histtype = 'stepfilled'
    if ylogscale:
        plt.yscale('log')

    for i, dat in enumerate(data):
        if i > 0:
            histtype = 'step'
            alpha = 1.0
        if clip_outlier:
            idx = dpr.is_outlier_percentile(dat)
            dat = dat[~idx]
        plt.hist(dat, bins=bins, normed=normed, alpha=alpha, histtype=histtype, label=legend[i])

    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.legend(loc=legend_loc)
    plt.tight_layout()
    plt.draw()
    if fig_dir:
        fig.savefig(os.path.join(fig_dir, plot_name + '.pdf'))
    plt.close(fig)
