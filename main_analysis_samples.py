import pofah.util.sample_factory as sf
import pofah.util.experiment as ex
import pofah.path_constants.sample_dict_file_parts_input as sdfi
import anpofah.sample_analysis.sample_analysis as saan


feature_analysis = False
constituents_analysis = True

# samples and their paths
sample_ids = ['qcdSideBis']

# read 
paths = sf.SamplePathDirFactory(sdfi.path_dict)
data = sf.read_inputs_to_event_sample_dict_from_dir(sample_ids, paths)

if feature_analysis:

	saan.analyze_feature(data, 'mJJ', plot_name='mJJ', fig_dir='fig')
	saan.analyze_feature(data, 'DeltaEtaJJ', plot_name='DeltaEtaJJ', fig_dir='fig')
	saan.analyze_feature(data, 'DeltaPhiJJ', plot_name='DeltaPhiJJ', fig_dir='fig')

if constituents_analysis:
	for sample_id in sample_ids:
		sample = data[sample_id]
		saan.analyze_constituents(sample, clip_outlier=True, plot_name_suffix='', fig_format='.png')
		#sample.convert_to_cartesian()
		#saan.analyze_constituents(sample, clip_outlier=True, plot_name_suffix='_cartesian', fig_format='.png')

