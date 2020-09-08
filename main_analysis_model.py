import pofah.util.experiment as ex
import pofah.path_constants.sample_dict_file_parts_selected as sds
import pofah.util.sample_factory as sf
import anpofah.model_analysis.roc_analysis as ra


# setup analysis inputs
run_n = 101
experiment = ex.Experiment(run_n).setup(model_analysis_dir=True)
paths = sf.SamplePathDirFactory(sds.path_dict).extend_base_path(experiment.run_dir)

BG_sample = 'qcdSideReco'
BG_SR_Sample = 'qcdSigAllReco'
SIG_samples = ['GtoWW15naReco', 'GtoWW25naReco', 'GtoWW35naReco', 'GtoWW45naReco']
#SIG_samples = ['GtoWW25naReco', 'qcdSigAllReco']
all_samples = [BG_sample, BG_SR_Sample] + SIG_samples

strategy_ids_total_loss = ['s1', 's2', 's3', 's4', 's5']
strategy_ids_kl_loss = ['kl1', 'kl2', 'kl3', 'kl4', 'kl5']

# read in data
data = sf.read_inputs_to_jet_sample_dict_from_dir(all_samples, paths)



# *****************************************
#					ROC
# *****************************************

# plot ROC for each signal
for SIG_sample in SIG_samples + [BG_SR_Sample]:
	ra.plot_ROC_loss_strategy(data[BG_sample], data[SIG_sample], strategy_ids_total_loss, title_suffix='_total_loss_', fig_dir=experiment.model_analysis_dir) 
	ra.plot_ROC_loss_strategy(data[BG_sample], data[SIG_sample], strategy_ids_kl_loss, title_suffix='_KL_loss_', fig_dir=experiment.model_analysis_dir) 


# plot binned ROC for each signal
mass_centers = [1500,2500,3500,4500]
for SIG_sample, mass_center in zip(SIG_samples, mass_centers):
	ra.plot_binned_ROC_loss_strategy(data[BG_sample], data[SIG_sample], mass_center, strategy_ids_total_loss, title_suffix='_total_loss_', fig_dir=experiment.model_analysis_dir)
	ra.plot_binned_ROC_loss_strategy(data[BG_sample], data[SIG_sample], mass_center, strategy_ids_kl_loss, title_suffix='_KL_loss_', fig_dir=experiment.model_analysis_dir)

# plot binned ROC for qcd signal region for all mass centers
for mass_center in zip(SIG_samples, mass_centers):
	ra.plot_binned_ROC_loss_strategy(data[BG_sample], data[BG_SR_Sample], mass_center, strategy_ids_total_loss, title_suffix='_total_loss_', fig_dir=experiment.model_analysis_dir)
	ra.plot_binned_ROC_loss_strategy(data[BG_sample], data[BG_SR_Sample], mass_center, strategy_ids_kl_loss, title_suffix='_KL_loss_', fig_dir=experiment.model_analysis_dir)



# *****************************************
#			LOSS DISTRIBUTION
# *****************************************

