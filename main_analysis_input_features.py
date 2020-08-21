import pofah.util.sample_factory as sf
import pofah.util.experiment as ex
import anpofah.plotting.feature_analysis as fa

# samples and their paths
sample_ids = ['qcdSigConcat', 'qcdSigSingle']
path_dict = {
	'base_dir' : '/eos/home-k/kiwoznia/dev/autoencoder_for_anomaly/convolutional_VAE/data/events',

	'sample_dir' : {
		'qcdSigConcat': 'qcd_sqrtshatTeV_13TeV_PU40_concat',
		'qcdSigSingle': 'qcd_sqrtshatTeV_13TeV_PU40'
	}
}

# read 
paths = sf.SamplePathDirFactory(path_dict)
data = sf.read_inputs_to_jet_sample_dict_from_dir(sample_ids, paths) # passing dummy experiment, TODO: make optional in sample factory

fa.plot_feature(data, 'mJJ', plot_name='mJJ', fig_dir='fig')
fa.plot_feature(data, 'DeltaEtaJJ', plot_name='DeltaEtaJJ', fig_dir='fig')
fa.plot_feature(data, 'DeltaPhiJJ', plot_name='DeltaPhiJJ', fig_dir='fig')
