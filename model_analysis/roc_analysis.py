import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics as skl
import os
import dadrah.selection.loss_strategy as ls
import pofah.jet_sample as js


def get_label_and_score_arrays(neg_class_losses, pos_class_losses):
    labels = []
    losses = []

    for neg_loss, pos_loss in zip(neg_class_losses, pos_class_losses):
        labels.append(np.concatenate([np.zeros(len(neg_loss)), np.ones(len(pos_loss))]))
        losses.append(np.concatenate([neg_loss, pos_loss]))

    return [labels, losses]


def get_mjj_binned_sample(sample, mjj_peak, window_pct=20):
    left_edge, right_edge = mjj_peak * (1. - window_pct / 100.), mjj_peak * (1. + window_pct / 100.)

    left_bin = sample[[sample['mJJ'] < left_edge]]
    center_bin = sample[[(sample['mJJ'] >= left_edge) & (sample['mJJ'] <= right_edge)]]
    right_bin = sample[[sample['mJJ'] > right_edge]]

    left_bin_ds = js.JetSample(sample.name, left_bin, title=sample.name + ' mJJ < ' + str(left_edge / 1000))
    center_bin_ds = js.JetSample(sample.name, center_bin, title=sample.name + ' ' + str(left_edge / 1000) + ' <= mJJ <= ' + str(right_edge / 1000))
    right_bin_ds = js.JetSample(sample.name, right_bin, title=sample.name + ' mJJ > ' + str(right_edge / 1000))

    return [left_bin_ds, center_bin_ds, right_bin_ds]


def get_mjj_binned_sample_center_bin(sample, mjj_peak, window_pct=20):
    left_edge, right_edge = mjj_peak * (1. - window_pct / 100.), mjj_peak * (1. + window_pct / 100.)
    data_center_bin = sample[[(sample['mJJ'] >= left_edge) & (sample['mJJ'] <= right_edge)]]
    return js.JetSample(sample.name, data_center_bin, title=sample.name + ' ' + str(left_edge / 1000) + ' <= mJJ <= ' + str(right_edge / 1000))


def plot_roc(neg_class_losses, pos_class_losses, legend, title='ROC', legend_loc='best', plot_name='ROC', fig_dir=None, xlim=None, log_x=True, fig_format='.png'):

    """
        :param:neg_class_losses: array or list of arrays with losses for samples of class 0
        :param:pos_class_losses: array or list of arrays with losses for samples of class 1
        :param:legend: string or list of strings for legend
        if lists, neg_class_losses, pos_class_losses and legend must be of same length
    """

    # set up matching roc curve inputs 
    if not isinstance(neg_class_losses, list): neg_class_losses = [neg_class_losses]
    if not isinstance(pos_class_losses, list): neg_class_losses = [pos_class_losses]
    if len(neg_class_losses) == 1 and len(pos_class_losses) > 1: 
        neg_class_losses = neg_class_losses*len(pos_class_losses)
    if not isinstance(legend, list): legend = [legend]


    class_labels, losses = get_label_and_score_arrays(neg_class_losses, pos_class_losses) # stack losses and create according labels
    aucs = []

    fig = plt.figure(figsize=(5, 5))

    for y_true, loss, label in zip(class_labels, losses, legend):
    	print(y_true)
    	print(loss)
    	print(np.isnan(loss).any())
    	print(np.isinf(loss).any())
    	print(np.argwhere(np.isnan(loss)))
    	print(np.argwhere(np.isinf(loss)))
    	print(len(np.argwhere(np.isnan(loss))))
    	print(len(np.argwhere(np.isinf(loss))))
    	fpr, tpr, threshold = skl.roc_curve(y_true, loss)
    	aucs.append(skl.roc_auc_score(y_true, loss))
    	if log_x:
    		plt.loglog(tpr, 1./fpr, label=label + " (auc " + "{0:.3f}".format(aucs[-1]) + ")")
    	else:
    		plt.semilogy(tpr, 1./fpr, label=label + " (auc " + "{0:.3f}".format(aucs[-1]) + ")")

    plt.grid()
    if xlim:
        plt.xlim(left=xlim)
    plt.xlabel('True positive rate')
    plt.ylabel('1 / False positive rate')
    legend = plt.legend(loc=legend_loc, handlelength=1.5)
    for leg in legend.legendHandles:
        leg.set_linewidth(2.2)
    plt.title(title)
    plt.tight_layout()
    if fig_dir:
        print('writing ROC plot to {}'.format(fig_dir))
        fig.savefig(os.path.join(fig_dir, plot_name + fig_format), bbox_inches='tight')
    plt.close(fig)
    return aucs



def plot_ROC_loss_strategy(bg_sample, sig_sample, strategy_ids, fig_dir, plot_name_suffix=None, log_x=True, fig_format='.png', loss_dict=ls.loss_strategy_dict):

    legend = [loss_dict[s_id].title_str for s_id in strategy_ids]
    plot_name = '_'.join(filter(None, ['ROC', sig_sample.name, plot_name_suffix]))
    # compute combined loss for each loss strategy
    neg_class_losses = [loss_dict[s_id](bg_sample) for s_id in strategy_ids]
    pos_class_losses = [loss_dict[s_id](sig_sample) for s_id in strategy_ids]
    plot_roc(neg_class_losses, pos_class_losses, legend=legend, title='ROC ' + sig_sample.title, plot_name=plot_name, fig_dir=fig_dir, log_x=log_x, fig_format=fig_format)


def plot_binned_ROC_loss_strategy(bg_sample, sig_sample, mass_center, strategy_ids, fig_dir, plot_name_suffix=None, log_x=True, fig_format='.png', loss_dict=ls.loss_strategy_dict):

    _, bg_center_bin_sample, _ = get_mjj_binned_sample(bg_sample, mass_center)
    _, sig_center_bin_sample, _ = get_mjj_binned_sample(sig_sample, mass_center)

<<<<<<< HEAD
	_, bg_center_bin_sample, _ = get_mjj_binned_sample(bg_sample, mass_center)
	_, sig_center_bin_sample, _ = get_mjj_binned_sample(sig_sample, mass_center)
	print('Making binned Mjj ROC for {}, BG/SIG sample size {}/{}'.format(plot_name_suffix,len(bg_center_bin_sample),len(sig_center_bin_sample)))
=======
    plot_name_suffix = 'mJJ_'+str(mass_center)+'_bin' + ('_' + plot_name_suffix if plot_name_suffix else '')
>>>>>>> 9b4058465124a6adac8c32e8ba90b25bfd353f0e
    
    plot_ROC_loss_strategy(bg_sample=bg_center_bin_sample, sig_sample=sig_center_bin_sample, strategy_ids=strategy_ids, \
            fig_dir=fig_dir, plot_name_suffix=plot_name_suffix, log_x=log_x, fig_format=fig_format, loss_dict=loss_dict)


def plot_binned_ROC(bg_samples, sig_samples, strategy, mass_center, fig_dir, plot_name_suffix, title_suffix='', legend=['run1', 'run2'], log_x=True):

    if not isinstance(bg_samples, list): bg_samples = [bg_samples]
    if not isinstance(sig_samples, list): sig_samples = [sig_samples]

    binned_bgs = [get_mjj_binned_sample_center_bin(s, mass_center) for s in bg_samples]
    binned_sigs = [get_mjj_binned_sample_center_bin(s, mass_center) for s in sig_samples]

    neg_class_losses = [strategy(b) for b in binned_bgs]
    pos_class_losses = [strategy(s) for s in binned_sigs]

    plot_roc(neg_class_losses, pos_class_losses, legend=legend, title='model comparison ROC binned ' + binned_sigs[0].name, log_x=True, plot_name='ROC_binned_logTPR_' + strategy.file_str + '_' + binned_sigs[0].name, fig_dir=fig_dir)


