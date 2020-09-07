import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics as skl
import os
import dadrah.selection.loss_strategy as ls


def get_label_and_score_arrays(neg_class_losses, pos_class_losses):
    labels = []
    losses = []

    for neg_loss, pos_loss in zip(neg_class_losses, pos_class_losses):
        labels.append(np.concatenate([np.zeros(len(neg_loss)), np.ones(len(pos_loss))]))
        losses.append(np.concatenate([neg_loss, pos_loss]))

    return [labels, losses]


def plot_roc(neg_class_losses, pos_class_losses, legend=[], title='ROC', legend_loc='best', plot_name='ROC', fig_dir=None, xlim=None, log_x=True):

    class_labels, losses = get_label_and_score_arrays(neg_class_losses, pos_class_losses) # neg_class_loss array same for all pos_class_losses

    aucs = []
    fig = plt.figure(figsize=(5, 5))

    for y_true, loss, label in zip(class_labels, losses, legend):
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
    plt.legend(loc=legend_loc)
    plt.tight_layout()
    plt.title(title)
    if fig_dir:
    	print('writing ROC plot to {}'.format(fig_dir))
    	fig.savefig(os.path.join(fig_dir, plot_name + '.png'), bbox_inches='tight')
    plt.close(fig)
    return aucs


def plot_ROC_loss_strategy(bg_sample, sig_sample, strategy_ids, fig_dir):

    legend = [ls.loss_strategy_dict[s_id].title_str for s_id in strategy_ids]
    # compute combined loss for each loss strategy
    neg_class_losses = [ls.loss_strategy_dict[s_id](bg_sample) for s_id in strategy_ids]
    pos_class_losses = [ls.loss_strategy_dict[s_id](sig_sample) for s_id in strategy_ids]
    plot_roc(neg_class_losses, pos_class_losses, legend=legend, title='ROC '+sig_sample.name, plot_name='ROC_'+sig_sample.name, fig_dir=fig_dir)
