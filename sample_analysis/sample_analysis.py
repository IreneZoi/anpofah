import anpofah.util.plotting_util as pu

def analyze_constituents(event_sample):
	p1, p2 = event_sample.get_particles()
	pu.plot_multihist(p1.transpose(), suptitle=event_sample.name, titles=event_sample.particle_feature_names, plot_name='hist_const1_'+event_sample.name, fig_dir='fig')
	pu.plot_multihist(p2.transpose(), suptitle=event_sample.name, titles=event_sample.particle_feature_names, plot_name='hist_const2_'+event_sample.name, fig_dir='fig')
