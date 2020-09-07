import pofah.util.experiment as ex
import pofah.path_constants.sample_dict_file_parts_selected as sds
import pofah.util.sample_factory as sf
import anpofah.model_analysis.roc_analysis as ra


# setup analysis inputs
run_n = 101
experiment = ex.Experiment(run_n).setup(model_analysis_dir=True)
paths = sf.SamplePathDirFactory(sds.path_dict).extend_base_path(experiment.run_dir)

BG_sample = 'qcdSideReco'
SIG_samples = ['GtoWW15naReco', 'GtoWW35naReco']
all_samples = [BG_sample] + SIG_samples

strategy_ids = ['s1', 's2', 's3', 's4', 's5']

# read in data
data = sf.read_inputs_to_jet_sample_dict_from_dir(all_samples, paths)

# plot roc plot for each signal
for SIG_sample in SIG_samples:
	ra.plot_ROC_loss_strategy(data[BG_sample], data[SIG_sample], strategy_ids, experiment.model_analysis_dir) 
