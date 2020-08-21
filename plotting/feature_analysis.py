import anpofah.util.plotting_util as pu


def plot_feature( sample_dict, feature_name, sample_names=None, fig_dir=None ):
	if not sample_names: 
		sample_names = sample_dict.keys()
	legend = [sample_dict[s].name for s in sample_names]
	feature = [ sample_dict[s][feature_name] for s in sample_names ]
	_ = pu.plot_hist(feature, legend=legend, xlabel=feature_name, title=r'distribution '+feature_name,legend_loc=(1.05,0), fig_dir=fig_dir)
