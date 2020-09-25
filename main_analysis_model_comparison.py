import pofah.util.experiment as ex
import pofah.path_constants.sample_dict_file_parts_reco as sdfr 
import pofah.util.sample_factory as sf
import anpofah.model_analysis.roc_analysis as ra
import anpofah.plotting.feature_analysis as fea
import dadrah.selection.loss_strategy as lost
import os


do_analyses = ['roc','loss']

BG_sample = 'qcdSideReco'
BG_SR_sample = 'qcdSigAllReco'
SIG_samples = ['GtoWW15naReco', 'GtoWW25naReco', 'GtoWW35naReco', 'GtoWW45naReco']
#SIG_samples = ['GtoWW25naReco', 'qcdSigAllReco']
mass_centers = [1500,2500,3500,4500]
all_samples = [BG_sample, BG_SR_sample] + SIG_samples

strategy_ids_total_loss = ['s1', 's2', 's3', 's4', 's5']
strategy_ids_kl_loss = ['kl1', 'kl2', 'kl3', 'kl4', 'kl5']
strategy = lost.loss_strategy_dict['s5'] # L1 & L2 > LT

run_model101 = 101
run_model46 = 46

experiment101 = ex.Experiment(run_model101)
experiment46 = ex.Experiment(run_model46)
experiment_result = ex.Experiment(param_dict={'$run1$': experiment101.run_dir, '$run2$': experiment46.run_dir}).setup(model_comparison_dir=True)

#read run 101 data
paths101 = sf.SamplePathDirFactory(sdfr.path_dict).update_base_path({'$run$': experiment101.run_dir})
data101 = sf.read_inputs_to_jet_sample_dict_from_dir(all_samples, paths101)

#read run 46 data
paths46 = sf.SamplePathDirFactory(sdfr.path_dict).update_base_path({'$run$': experiment46.run_dir})
data46 = sf.read_inputs_to_jet_sample_dict_from_dir(all_samples, paths46)


if 'roc' in do_analyses:
	# *****************************************
	#					ROC
	# *****************************************
	
	# plot binned ROC comparing 2 models for a single strategy
	for SIG_sample, mass_center in zip(SIG_samples, mass_centers):
		legend = [data101[SIG_sample].name + ' particle VAE', data101[SIG_sample].name + ' image VAE']
		ra.plot_binned_ROC([data101[BG_sample], data46[BG_sample]], [data101[SIG_sample], data46[SIG_sample]], strategy, mass_center, legend=legend, fig_dir=experiment_result.model_comparison_dir_roc, plot_name_suffix='total_loss')


if 'loss' in do_analyses:
# *****************************************
#			LOSS DISTRIBUTION
# *****************************************
	pass

