import pofah.util.sample_factory as sf
import pofah.util.experiment as ex
import pofah.path_constants.sample_dict_file_parts_input as sdfi
import anpofah.sample_analysis.sample_analysis as saan


feature_analysis = False
constituents_analysis = True
mjj_cut = True

# samples and their paths
sample_ids_grav = ['GtoWW15na','GtoWW15br','GtoWW25na','GtoWW25br','GtoWW35na','GtoWW35br','GtoWW45na','GtoWW45br',]
#sample_ids_azzz = ['AtoHZ15', 'AtoHZ20', 'AtoHZ25', 'AtoHZ30', 'AtoHZ35', 'AtoHZ40', 'AtoHZ45']
sample_ids_azzz = ['AtoHZ15', 'AtoHZ25', 'AtoHZ35', 'AtoHZ45']
sample_ids_qcd = ['qcdSide', 'qcdSideExt', 'qcdSig', 'qcdSigExt']
sample_ids_qcd_sb_vs_sr = ['qcdSide', 'qcdSig']
sample_ids_qcd_grav = sample_ids_qcd_sb_vs_sr + sample_ids_grav
sample_ids_qcd_azzz = sample_ids_qcd_sb_vs_sr + sample_ids_azzz

paths = sf.SamplePathDirFactory(sdfi.path_dict)

if feature_analysis:

	for (sample_ids, suffix) in zip([sample_ids_qcd_sb_vs_sr, sample_ids_qcd_grav, sample_ids_qcd_azzz, sample_ids_qcd],['sb_vs_sr', 'vs_grav', 'vs_azzz', 'sb_vs_sr_ext']):

		# read 
		data = sf.read_inputs_to_event_sample_dict_from_dir(sample_ids, paths, max_N=10e6, apply_mjj_cut=mjj_cut)

		saan.analyze_feature(data, 'mJJ', plot_name='mJJ_new_qcd_'+suffix, fig_dir='fig/merged_data_for_VAE', first_is_bg=True, legend_loc='best', fig_format='.png')
		saan.analyze_feature(data, 'DeltaEtaJJ', plot_name='DeltaEtaJJ_new_qcd_'+suffix, fig_dir='fig/merged_data_for_VAE', first_is_bg=True, legend_loc='best', fig_format='.png')
		saan.analyze_feature(data, 'DeltaPhiJJ', plot_name='DeltaPhiJJ_new_qcd_'+suffix, fig_dir='fig/merged_data_for_VAE', first_is_bg=True, legend_loc='best', fig_format='.png')


if constituents_analysis:

	# read 
	sample_ids = sample_ids_qcd + sample_ids_grav + sample_ids_azzz
	data = sf.read_inputs_to_event_sample_dict_from_dir(sample_ids, paths, max_N=10e6, apply_mjj_cut=mjj_cut)

	for sample_id in sample_ids:

		sample = data[sample_id]
		saan.analyze_constituents(sample, clip_outlier=True, fig_dir='fig/merged_data_for_VAE', fig_format='.png')
		#sample.convert_to_cartesian()
		#saan.analyze_constituents(sample, clip_outlier=True, plot_name_suffix='_cartesian', fig_format='.png')


