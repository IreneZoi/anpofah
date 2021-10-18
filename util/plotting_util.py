import matplotlib.pyplot as plt
from matplotlib import colors
import os
import numpy as np
import mplhep as hep

import anpofah.util.data_preprocessing as dpr


# Load CMS style sheet
plt.style.use(hep.style.CMS)
palette = ['#3E96A1', '#EC4E20', '#FF9505', '#713E5A', '#D62828', '#5F0F40']


def subplots_rows_cols(n, single_row=False):
    ''' get number of subplot rows and columns needed to plot n histograms in one figure '''
    if single_row:
        return 1, n
    return int(np.round(np.sqrt(n))), int(np.ceil(np.sqrt(n)))


def plot_hist(data, bins=100, xlabel='x', ylabel='num frac', title='histogram', plot_name='plot', fig_dir=None, legend=[], ylogscale=True, normed=True, ylim=None, legend_loc='best', xlim=None, clip_outlier=False, fig_format='.png'):
    fig = plt.figure(figsize=(6, 4))
    if clip_outlier:
        data = [dpr.clip_outlier(dat) for dat in data]
    counts, edges = plot_hist_on_axis(plt.gca(), data, bins=bins, xlabel=xlabel, ylabel=ylabel, title=title, legend=legend, ylogscale=ylogscale, normed=normed, ylim=ylim, xlim=xlim)
    if legend:
        plt.legend(loc=legend_loc)
    plt.tight_layout()
    if fig_dir is not None:
        fig.savefig(os.path.join(fig_dir, plot_name + fig_format))
    else:
        plt.show();
    plt.close(fig)
    return counts, edges


def plot_multihist(data, bins=100, suptitle='histograms', titles=[], clip_outlier=False, plot_name='histograms', fig_dir=None, fig_format='.pdf'):
    ''' plot len(data) histograms plots on same figure 
        data = list of features to plot (each element is flattened before plotting)
    '''
    rows_n, cols_n = subplots_rows_cols(len(data))
    fig, axs = plt.subplots(nrows=rows_n, ncols=cols_n, figsize=(9,9))
    for ax, dat, title in zip(axs.flat, data, titles):
        if clip_outlier:
            dat = dpr.clip_outlier(dat.flatten())
        plot_hist_on_axis(ax, dat.flatten(), bins=bins, title=title)
    [a.axis('off') for a in axs.flat[len(data):]] # turn off unused subplots
    plt.suptitle(suptitle)
    plt.tight_layout(rect=(0, 0, 1, 0.95))
    if fig_dir is not None:
        fig.savefig(os.path.join(fig_dir, plot_name + fig_format))
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
    return counts, edges


def plot_hist_2d(x, y, xlabel='x', ylabel='num frac', title='histogram', plot_name='hist2d', fig_dir=None, legend=[], ylogscale=True, normed=True, ylim=None, legend_loc='best', xlim=None, clip_outlier=False):
    
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
    
    
def plot_hist_2d_on_axis(ax, x, y, xlabel, ylabel, title):
    im = ax.hist2d(x, y, bins=100, norm=colors.LogNorm())
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    return im


def plot_bg_vs_sig(data, sample_names, bins=100, xlabel='x', ylabel='fraction events', title='histogram', \
    plot_name='plot', fig_dir=None, legend=['bg','sig'], ylogscale=True, normed=True, legend_loc='best', \
    clip_outlier=False, xlim=None, fig_format='.pdf', histtype_sig='step'):
    '''
    plots feature distribution treating first data-array as backround and rest of arrays as signal
    :param data: list/array of N elements where first element is assumed to be background and elements 2..N-1 assumed to be signal. all elements = array of length M
    '''

    qcd_idx = [i for (i,s) in enumerate(sample_names) if 'qcd' in s][0]

    fig = plt.figure(figsize=(7, 5))
    if ylogscale:
        plt.yscale('log')

    for i, (dat, col) in enumerate(zip(data,palette)):
        if clip_outlier:
            idx = dpr.is_outlier_percentile(dat)
            dat = dat[~idx]
        if i == qcd_idx:
            plt.hist(dat, bins=bins, density=normed, alpha=0.5, histtype='stepfilled', label=legend[i], color=col)
        else:
            plt.hist(dat, bins=bins, density=normed, alpha=1.0, histtype=histtype_sig, label=legend[i], color=col)

    if xlim:
        plt.xlim(xlim)
    plt.ylabel(ylabel, fontsize=14)
    plt.xlabel(xlabel, fontsize=14)
    #plt.title(title, fontsize=18)
    handles, labels = plt.gca().get_legend_handles_labels()
    lgd = fig.legend(handles, labels, bbox_to_anchor=(0.5,-0.05), loc="lower center", ncol=len(data), fontsize=16)
    plt.tight_layout()
    plt.draw()
    if fig_dir:
        fig.savefig(os.path.join(fig_dir, plot_name + fig_format), bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close(fig)


def plot_m_features_for_n_samples(data, feature_names, sample_names, bins=100, suptitle=None, clip_outlier=False, normed=True, \
        ylogscale=True, single_row=False, plot_name='multihist', fig_dir='fig', fig_format='.pdf', fig_size=(7,7), bg_name=None, histtype_bg='stepfilled'):
    '''
        plot multiple features for multiple samples as 1D histograms in one figure
        :param data: list of J ndarrays of K features with each N values
        :param bg_name: if not None, one sample will be treated as background and plotted differently
    '''

    # if one sample is to be treated as background sample
    if bg_name is not None:
        bg_idx = [i for (i,s) in enumerate(sample_names) if bg_name in s][0]
    else:
        bg_idx = -1

    rows_n, cols_n = subplots_rows_cols(len(feature_names), single_row=single_row)
    fig, axs = plt.subplots(nrows=rows_n, ncols=cols_n, figsize=fig_size)

    # for each feature
    for k, (ax, xlabel) in enumerate(zip(axs.flat, feature_names)):
        # loop through datasets
        for i, (dat, col) in enumerate(zip(data,palette)): 
            if i == bg_idx:
                ax.hist(dat[k], bins=bins, density=True, alpha=0.5, histtype=histtype_bg, label=sample_names[i], color=col)
            else:
                ax.hist(dat[k], bins=bins, density=True, alpha=1.0, histtype='step', linewidth=1.3, label=sample_names[i], color=col)
        if ylogscale:
            ax.set_yscale('log', nonpositive='clip')
        ax.set_xlabel(xlabel)
    
    axs[0].set_ylabel('fraction events')
    #plt.legend(bbox_to_anchor=(0.5,-0.1), loc="upper center", mode='expand', ncol=len(data))
    handles, labels = ax.get_legend_handles_labels()
    lgd = fig.legend(handles, labels, bbox_to_anchor=(0.5,-0.1), loc="lower center", ncol=len(data))
    if suptitle is not None:
        plt.suptitle(suptitle)
    plt.tight_layout(rect=(0, 0, 1, 0.95))
    print('writing figure to ' + os.path.join(fig_dir, plot_name + fig_format))
    fig.savefig(os.path.join(fig_dir, plot_name + fig_format), bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close(fig)

