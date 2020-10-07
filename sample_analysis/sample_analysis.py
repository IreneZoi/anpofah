import anpofah.util.plotting_util as pu

def analyze_constituents(event_sample, plot_name_suffix=''):
	''' analyze particles of jet1 and jet2 '''
	p1, p2 = event_sample.get_particles()
	pu.plot_multihist(p1.transpose(), suptitle=event_sample.name, titles=event_sample.particle_feature_names, plot_name='hist_const1_'+event_sample.name+plot_name_suffix, fig_dir='fig')
	pu.plot_multihist(p2.transpose(), suptitle=event_sample.name, titles=event_sample.particle_feature_names, plot_name='hist_const2_'+event_sample.name+plot_name_suffix, fig_dir='fig')


def analyze_feature(sample_dict, feature_name, sample_names=None, plot_name='plot', fig_dir=None, first_is_bg=True, clip_outlier=False, map_fun=None, ylogscale=True, xlim=None, fig_format='.pdf'):
	''' for each sample in sample_dict: analyze feature of dijet 
		if map_fun is given, process map_fun(feature) before analysis
	'''
	if not sample_names: 
		sample_names = sample_dict.keys()
	legend = [sample_dict[s].name for s in sample_names]
	if map_fun:
		feature = [map_fun(sample_dict[s]) for s in sample_names]
	else:
		feature = [sample_dict[s][feature_name] for s in sample_names]
	if first_is_bg:
		pu.plot_bg_vs_sig(feature, legend=legend, xlabel=feature_name, title=r'distribution '+feature_name,legend_loc=(1.05,0), plot_name=plot_name, fig_dir=fig_dir, clip_outlier=clip_outlier, ylogscale=ylogscale, xlim=xlim, fig_format=fig_format)
	else:
		_ = pu.plot_hist(feature, legend=legend, xlabel=feature_name, title=r'distribution '+feature_name,legend_loc=(1.05,0), plot_name=plot_name, fig_dir=fig_dir, ylogscale=ylogscale)
