import numpy as np
import os
import matplotlib.pyplot as plt
import anpofah.util.plotting_util as pu


def analyze_constituents(event_sample, clip_outlier=False, title_suffix='', plot_name_suffix='', fig_dir='fig', fig_format='.pdf'):
    ''' analyze particles of jet1 and jet2 '''
    p1, p2 = event_sample.get_particles()
    pu.plot_multihist(p1.transpose(), suptitle=' '.join([event_sample.name, 'particles J1', title_suffix]), titles=event_sample.particle_feature_names, clip_outlier=clip_outlier, plot_name='_'.join(['hist_const1', event_sample.name, plot_name_suffix]), fig_dir=fig_dir, fig_format=fig_format)
    pu.plot_multihist(p2.transpose(), suptitle=' '.join([event_sample.name, 'particles J2', title_suffix]), titles=event_sample.particle_feature_names, clip_outlier=clip_outlier, plot_name='_'.join(['hist_const2', event_sample.name, plot_name_suffix]), fig_dir=fig_dir, fig_format=fig_format)


def analyze_constituents_bg_vs_sig(event_sample_dict, sample_names=None, fig_dir='fig', fig_format='.pdf'):

    '''
        plot multihist bg vs sig for all constituent features and multiple signal samples
        assumes that first element in dict is bg!
    '''

    sample_names = sample_names or list(event_sample_dict.keys())
    qcd_idx = [i for (i,s) in enumerate(sample_names) if 'qcd' in s][0]
    p_feature_names = [r'$\eta$', r'$\phi$', 'pt']
    plot_name = 'constituent_distribution'

    # import ipdb; ipdb.set_trace()

    p1 = [event_sample_dict[s_name].get_particles(jet_n=0).transpose(2,1,0).reshape(len(p_feature_names), -1) for s_name in sample_names] # [J_samples x [K_features x N_events * 100 particles]]
    p2 = [event_sample_dict[s_name].get_particles(jet_n=1).transpose(2,1,0).reshape(len(p_feature_names), -1) for s_name in sample_names] # [J_samples x [K_features x N_events * 100 particles]]

    pu.plot_bg_vs_sig_multihist(data=p1, feature_names=p_feature_names, sample_names=sample_names, single_row=True, plot_name=plot_name+'_p1', fig_dir=fig_dir, fig_format='.png', histtype_sig='step', fig_size=(12,6))
    pu.plot_bg_vs_sig_multihist(data=p2, feature_names=p_feature_names, sample_names=sample_names, single_row=True, plot_name=plot_name+'_p2', fig_dir=fig_dir, fig_format='.png', histtype_sig='step', fig_size=(12,6))



def analyze_feature(sample_dict, feature_name, sample_names=None, title_suffix='', plot_name='plot', fig_dir=None, bg_vs_sig=True, clip_outlier=False, map_fun=None, legend_loc=(1.05,0), ylogscale=True, xlim=None, normed=True, fig_format='.pdf'):
    ''' for each sample (event or jet) in sample_dict: analyze feature of dijet 
        if map_fun is given, process map_fun(feature) before analysis
    '''
    sample_names = sample_names or list(sample_dict.keys())
    legend = [sample_dict[s].name for s in sample_names]
    if map_fun:
        feature = [map_fun(sample_dict[s]) for s in sample_names]
    else:
        feature = [sample_dict[s][feature_name] for s in sample_names]
    if bg_vs_sig:
        pu.plot_bg_vs_sig(feature, sample_names, legend=legend, xlabel=feature_name, title=' '.join([r'distribution ', feature_name, title_suffix]), legend_loc=legend_loc, plot_name=plot_name, fig_dir=fig_dir, clip_outlier=clip_outlier, ylogscale=ylogscale, xlim=xlim, fig_format=fig_format)
    else:
        return pu.plot_hist(feature, legend=legend, xlabel=feature_name, title=' '.join([r'distribution ', feature_name, title_suffix]), legend_loc=legend_loc, plot_name=plot_name, fig_dir=fig_dir, ylogscale=ylogscale, normed=normed, clip_outlier=clip_outlier, xlim=xlim, fig_format=fig_format)


def analyze_feature_2D(sample_dict, feature_name_1, feature_name_2, sample_names=None, title_suffix='', plot_name='hist2D', fig_dir=None, clip_outlier=False, map_fun_1=None, map_fun_2=None, fig_format='.png'):
    ''' for each sample in sample_dict: plot 2D histogram of feature_1 and feature_2
        if map_fun_1 and/or map_fun_2 is given, apply mapping to sample before plotting
    '''
    if not sample_names: 
        sample_names = sample_dict.keys()
    legend = [sample_dict[s].name for s in sample_names]

    if map_fun_1:
        feature_1 = [map_fun_1(sample_dict[s]) for s in sample_names]
    else:
        feature_1 = [sample_dict[s][feature_name_1] for s in sample_names]
    if map_fun_2:
        feature_2 = [map_fun_2(sample_dict[s]) for s in sample_names]
    else:
        feature_2 = [sample_dict[s][feature_name_2] for s in sample_names]

    for name, f1, f2 in zip(sample_names, feature_1, feature_2):
        title = ' '.join(['distribution', name, feature_name_1, 'vs', feature_name_2, title_suffix])
        plot = '_'.join([plot_name, feature_name_1, feature_name_2, name])
        pu.plot_hist_2d(f1, f2, xlabel=feature_name_1, ylabel=feature_name_2, title=title, plot_name=plot, fig_dir=fig_dir, legend=legend, clip_outlier=clip_outlier)
