import pofah.util.experiment as ex
import pofah.path_constants.sample_dict_file_parts_reco as sdfr 
import pofah.util.sample_factory as sf
import anpofah.model_analysis.roc_analysis as ra
import anpofah.sample_analysis.sample_analysis as saan
import dadrah.selection.loss_strategy as lost
import anpofah.util.sample_names as samp

import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import sklearn.metrics as skl
import os


def plot_roc(neg_class_losses, pos_class_losses_na, pos_class_losses_br, legend, title='ROC', legend_loc='best', plot_name='ROC', fig_dir=None, x_lim=None, log_x=True, fig_format='.png'):

    class_labels_na, losses_na = ra.get_label_and_score_arrays(neg_class_losses, pos_class_losses_na) # stack losses and create according labels per strategy
    class_labels_br, losses_br = ra.get_label_and_score_arrays(neg_class_losses, pos_class_losses_br) # stack losses and create according labels per strategy
    class_labels, losses = class_labels_na + class_labels_br, losses_na + losses_br

    colors = ['blue']*len(neg_class_losses) + ['darkorange']*len(neg_class_losses)
    styles = ['dashed', 'dashdot', 'dotted']*2

    aucs = []
    fig = plt.figure(figsize=(5, 5))

    for y_true, loss, label, color, style in zip(class_labels, losses, legend, colors, styles):
        fpr, tpr, threshold = skl.roc_curve(y_true, loss)
        aucs.append(skl.roc_auc_score(y_true, loss))
        if log_x:
            plt.loglog(tpr, 1./fpr, label=label + " (auc " + "{0:.3f}".format(aucs[-1]) + ")", linestyle=style, color=color)
        else:
            plt.semilogy(tpr, 1./fpr, label=label + " (auc " + "{0:.3f}".format(aucs[-1]) + ")", linestyle=style, color=color)
            plt.semilogy(np.linspace(0, 1, num=100), 1./np.linspace(0, 1, num=100), linewidth=1., linestyle='solid', color='silver')
    plt.grid()
    if x_lim:
        plt.xlim(left=x_lim)
    plt.xlabel('True positive rate')
    plt.ylabel('1 / False positive rate')
    plt.legend(loc=legend_loc)
    plt.tight_layout()
    plt.title(title)
    if fig_dir:
        print('writing ROC plot to {}'.format(fig_dir))
        fig.savefig(os.path.join(fig_dir, plot_name + fig_format), bbox_inches='tight')
    plt.close(fig)
    return aucs



def plot_mass_center_ROC(bg_sample, sig_sample_na, sig_sample_br, mass_center, plot_name_suffix=None, fig_dir='fig', fig_format='.png'):
    ''' 
        plot ROC for narrow and broad signal (color)
        reco, kl and total combined loss (marker)
    ''' 

    _, bg_center_bin_sample, _ = ra.get_mjj_binned_sample(bg_sample, mass_center)
    _, sig_center_bin_sample_na, _ = ra.get_mjj_binned_sample(sig_sample_na, mass_center)
    _, sig_center_bin_sample_br, _ = ra.get_mjj_binned_sample(sig_sample_br, mass_center)

    strategy_ids = ['r5', 'kl5', 'rk5']
    title_strategy_suffix = 'loss J1 && loss J2 > LT'
    legend = [s_id + ' ' + sig_type for sig_type in ('na', 'br') for s_id in ('Reco', r'$D_{KL}$', r'Reco + 10*$D_{KL}$')]
    plot_name = '_'.join(filter(None, ['ROC', sig_sample_na.name.replace('Reco', 'br'), plot_name_suffix]))
    title = r'$G_{{RS}} \to WW \, m_{{G}} = {} TeV$'.format(mass_center/1000)
    log_x = False
    x_lim = None

    neg_class_losses = [lost.loss_strategy_dict[s_id](bg_center_bin_sample) for s_id in strategy_ids]
    pos_class_losses_na = [lost.loss_strategy_dict[s_id](sig_center_bin_sample_na) for s_id in strategy_ids]
    pos_class_losses_br = [lost.loss_strategy_dict[s_id](sig_center_bin_sample_br) for s_id in strategy_ids]

    plot_roc(neg_class_losses, pos_class_losses_na, pos_class_losses_br, legend=legend, title=title, plot_name=plot_name, fig_dir=fig_dir, x_lim=x_lim, log_x=log_x, fig_format=fig_format)



if __name__ == '__main__':    

    # setup analysis inputs
    run_n = 113
    # set background sample to use (sideband or signalregion)
    BG_sample = samp.BG_SR_sample
    mass_centers = [1500, 2500, 3500, 4500]


    # set up analysis outputs 
    experiment = ex.Experiment(run_n).setup(model_analysis_dir=True)
    paths = sf.SamplePathDirFactory(sdfr.path_dict).update_base_path({'$run$': experiment.run_dir})
    print('Running analysis on experiment {}, plotting results to {}'.format(run_n, experiment.model_analysis_dir))
    
    # read in data
    data = sf.read_inputs_to_jet_sample_dict_from_dir(samp.all_samples, paths, read_n=None)

    # Load CMS style sheet
    plt.style.use(hep.style.CMS)

    # *****************************************
    #                   ROC
    # *****************************************
    # for each mass center
    for SIG_sample_na, SIG_sample_br, mass_center in zip(samp.SIG_samples_na, samp.SIG_samples_br, mass_centers):
        plot_mass_center_ROC(data[BG_sample], data[SIG_sample_na], data[SIG_sample_br], mass_center, fig_dir=experiment.model_analysis_dir_roc)
