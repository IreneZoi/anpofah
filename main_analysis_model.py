import pofah.util.experiment as ex
import pofah.path_constants.sample_dict_file_parts_reco as sdfr 
import pofah.util.sample_factory as sf
import anpofah.model_analysis.roc_analysis as ra
import anpofah.sample_analysis.sample_analysis as saan
import dadrah.selection.loss_strategy as lost


# setup analysis inputs
do_analyses = ['loss_combi']
run_n = 502
fig_format = '.png'
experiment = ex.Experiment(run_n).setup(model_analysis_dir=True)
paths = sf.SamplePathDirFactory(sdfr.path_dict).update_base_path({'$run$': experiment.run_dir})

BG_sample = 'qcdSideAllReco'
BG_SR_sample = 'qcdSigAllReco'
SIG_samples = ['GtoWW15naReco', 'GtoWW25naReco', 'GtoWW35naReco', 'GtoWW45naReco']
SIG_samples_br = ['GtoWW15brReco', 'GtoWW25brReco', 'GtoWW35brReco', 'GtoWW45brReco']
#SIG_samples = ['GtoWW25naReco', 'qcdSigAllReco']
all_samples = [BG_sample, BG_SR_sample] + SIG_samples + SIG_samples_br

strategy_ids_total_loss = ['s1', 's2', 's3', 's4', 's5']
strategy_ids_reco_kl_loss = ['rk5']
strategy_ids_kl_loss = ['kl1', 'kl2', 'kl3', 'kl4', 'kl5']

# read in data
data = sf.read_inputs_to_jet_sample_dict_from_dir(all_samples, paths)


# *****************************************
#					ROC
# *****************************************
if 'roc' in do_analyses:

	# plot ROC for each signal
	for SIG_sample in SIG_samples + [BG_SR_sample]:
		ra.plot_ROC_loss_strategy(data[BG_sample], data[SIG_sample], strategy_ids_reco_kl_loss, plot_name_suffix='reco_kl_loss', fig_dir=experiment.model_analysis_dir_roc) 
		ra.plot_ROC_loss_strategy(data[BG_sample], data[SIG_sample], strategy_ids_total_loss, plot_name_suffix='total_loss', fig_dir=experiment.model_analysis_dir_roc) 
		ra.plot_ROC_loss_strategy(data[BG_sample], data[SIG_sample], strategy_ids_kl_loss, plot_name_suffix='_KL_loss_', fig_dir=experiment.model_analysis_dir_roc) 

	# plot binned ROC for each narrow signal
	mass_centers = [1500,2500,3500,4500]
	for SIG_sample, mass_center in zip(SIG_samples, mass_centers):
		ra.plot_binned_ROC_loss_strategy(data[BG_sample], data[SIG_sample], mass_center, strategy_ids_reco_kl_loss, plot_name_suffix='reco_kl_loss_na', fig_dir=experiment.model_analysis_dir_roc)
		ra.plot_binned_ROC_loss_strategy(data[BG_sample], data[SIG_sample], mass_center, strategy_ids_total_loss, plot_name_suffix='total_loss_na', fig_dir=experiment.model_analysis_dir_roc)
		ra.plot_binned_ROC_loss_strategy(data[BG_sample], data[SIG_sample], mass_center, strategy_ids_kl_loss, plot_name_suffix='KL_loss_na', fig_dir=experiment.model_analysis_dir_roc)

	# plot binned ROC for each broad signal
	mass_centers = [1500,2500,3500,4500]
	for SIG_sample, mass_center in zip(SIG_samples_br, mass_centers):
		ra.plot_binned_ROC_loss_strategy(data[BG_sample], data[SIG_sample], mass_center, strategy_ids_reco_kl_loss, plot_name_suffix='reco_kl_loss_br', fig_dir=experiment.model_analysis_dir_roc)
		ra.plot_binned_ROC_loss_strategy(data[BG_sample], data[SIG_sample], mass_center, strategy_ids_total_loss, plot_name_suffix='total_loss_br', fig_dir=experiment.model_analysis_dir_roc)
		ra.plot_binned_ROC_loss_strategy(data[BG_sample], data[SIG_sample], mass_center, strategy_ids_kl_loss, plot_name_suffix='KL_loss_br', fig_dir=experiment.model_analysis_dir_roc)

if 'roc_qcd_sb_vs_sr' in do_analyses:
	# plot binned ROC for qcd signal region for all mass centers
	for mass_center in mass_centers:
		ra.plot_binned_ROC_loss_strategy(data[BG_sample], data[BG_SR_sample], mass_center, strategy_ids_reco_kl_loss, plot_name_suffix='reco_kl_loss', fig_dir=experiment.model_analysis_dir_roc)
		ra.plot_binned_ROC_loss_strategy(data[BG_sample], data[BG_SR_sample], mass_center, strategy_ids_total_loss, plot_name_suffix='total_loss', fig_dir=experiment.model_analysis_dir_roc)
		#ra.plot_binned_ROC_loss_strategy(data[BG_sample], data[BG_SR_sample], mass_center, strategy_ids_kl_loss, plot_name_suffix='KL_loss', fig_dir=experiment.model_analysis_dir_roc)


# *****************************************
#			LOSS DISTRIBUTION
# *****************************************
if 'loss' in do_analyses:
	# plot loss distribution for qcd side vs signals
	saan.analyze_feature(data, 'j1TotalLoss', sample_names=[BG_sample]+SIG_samples, plot_name='loss_distr_TotalJ1_qcdSB_vs_sig', fig_dir=experiment.model_analysis_dir_loss, fig_format=fig_format)
	saan.analyze_feature(data, 'j2TotalLoss', sample_names=[BG_sample]+SIG_samples, plot_name='loss_distr_TotalJ2_qcdSB_vs_sig', fig_dir=experiment.model_analysis_dir_loss, fig_format=fig_format)
	saan.analyze_feature(data, 'j1KlLoss', sample_names=[BG_sample]+SIG_samples, plot_name='loss_distr_KL1_qcdSB_vs_sig', fig_dir=experiment.model_analysis_dir_loss, clip_outlier=True, fig_format=fig_format)
	saan.analyze_feature(data, 'j2KlLoss', sample_names=[BG_sample]+SIG_samples, plot_name='loss_distr_KL2_qcdSB_vs_sig', fig_dir=experiment.model_analysis_dir_loss, clip_outlier=True, fig_format=fig_format)

	# plot loss distribution for qcd signal region vs signals
	saan.analyze_feature(data, 'j1TotalLoss', sample_names=[BG_SR_sample]+SIG_samples, plot_name='loss_distr_TotalJ1_qcdSR_vs_sig', fig_dir=experiment.model_analysis_dir_loss, fig_format=fig_format)
	saan.analyze_feature(data, 'j2TotalLoss', sample_names=[BG_SR_sample]+SIG_samples, plot_name='loss_distr_TotalJ2_qcdSR_vs_sig', fig_dir=experiment.model_analysis_dir_loss, fig_format=fig_format)
	saan.analyze_feature(data, 'j1KlLoss', sample_names=[BG_SR_sample]+SIG_samples, plot_name='loss_distr_KL1_qcdSR_vs_sig', fig_dir=experiment.model_analysis_dir_loss, clip_outlier=True, fig_format=fig_format)
	saan.analyze_feature(data, 'j2KlLoss', sample_names=[BG_SR_sample]+SIG_samples, plot_name='loss_distr_KL2_qcdSR_vs_sig', fig_dir=experiment.model_analysis_dir_loss, clip_outlier=True, fig_format=fig_format)

	# plot loss distribution for qcd side vs qcd signal region
	saan.analyze_feature(data, 'j1TotalLoss', sample_names=[BG_sample, BG_SR_sample], plot_name='loss_distr_TotalJ1_qcdSB_vs_qcdSR', fig_dir=experiment.model_analysis_dir_loss, fig_format=fig_format)
	saan.analyze_feature(data, 'j2TotalLoss', sample_names=[BG_sample, BG_SR_sample], plot_name='loss_distr_TotalJ2_qcdSB_vs_qcdSR', fig_dir=experiment.model_analysis_dir_loss, fig_format=fig_format)
	saan.analyze_feature(data, 'j1KlLoss', sample_names=[BG_sample, BG_SR_sample], plot_name='loss_distr_KL1_qcdSB_vs_qcdSR', fig_dir=experiment.model_analysis_dir_loss, clip_outlier=True, fig_format=fig_format)
	saan.analyze_feature(data, 'j2KlLoss', sample_names=[BG_sample, BG_SR_sample], plot_name='loss_distr_KL2_qcdSB_vs_qcdSR', fig_dir=experiment.model_analysis_dir_loss, clip_outlier=True, fig_format=fig_format)


# *****************************************
#			COMBINED LOSS DISTRIBUTION
# *****************************************
if 'loss_combi' in do_analyses:
	loss_combi_ids = ['s3', 's4', 's5', 'rk5']
	for loss_id in loss_combi_ids:
		loss_strategy = lost.loss_strategy_dict[loss_id]
		# plot loss distribution for qcd side vs signals
		saan.analyze_feature(data, loss_strategy.title_str, map_fun=loss_strategy, sample_names=[BG_sample]+SIG_samples, plot_name='loss_distr_'+loss_strategy.file_str+'_qcdSB_vs_sig_na', fig_dir=experiment.model_analysis_dir_loss, fig_format=fig_format)
		# plot loss distribution for qcd signal region vs signals
		saan.analyze_feature(data, loss_strategy.title_str, map_fun=loss_strategy, sample_names=[BG_SR_sample]+SIG_samples, plot_name='loss_distr_'+loss_strategy.file_str+'_qcdSR_vs_sig_na', fig_dir=experiment.model_analysis_dir_loss, fig_format=fig_format)
		# plot loss distribution for qcd side vs qcd signal region
		saan.analyze_feature(data, loss_strategy.title_str, map_fun=loss_strategy, sample_names=[BG_sample, BG_SR_sample], plot_name='loss_distr_'+loss_strategy.file_str+'_qcdSB_vs_qcdSR', fig_dir=experiment.model_analysis_dir_loss, fig_format=fig_format)
		#
		saan.analyze_feature(data, loss_strategy.title_str, map_fun=loss_strategy, sample_names=[BG_sample]+SIG_samples_br, plot_name='loss_distr_'+loss_strategy.file_str+'_qcdSB_vs_sig_br', fig_dir=experiment.model_analysis_dir_loss, fig_format=fig_format)
		# plot loss distribution for qcd signal region vs signals
		saan.analyze_feature(data, loss_strategy.title_str, map_fun=loss_strategy, sample_names=[BG_SR_sample]+SIG_samples_br, plot_name='loss_distr_'+loss_strategy.file_str+'_qcdSR_vs_sig_br', fig_dir=experiment.model_analysis_dir_loss, fig_format=fig_format)