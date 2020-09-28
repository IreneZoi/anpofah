import anpofah.util.plotting_util as pu

def analyze_constituents(event_sample, plot_name_suffix=''):
	p1, p2 = event_sample.get_particles()
	pu.plot_multihist(p1.transpose(), suptitle=event_sample.name, titles=event_sample.particle_feature_names, plot_name='hist_const1_'+event_sample.name+plot_name_suffix, fig_dir='fig')
	pu.plot_multihist(p2.transpose(), suptitle=event_sample.name, titles=event_sample.particle_feature_names, plot_name='hist_const2_'+event_sample.name+plot_name_suffix, fig_dir='fig')
