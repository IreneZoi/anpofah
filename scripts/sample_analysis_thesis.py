import pofah.path_constants.sample_dict_file_parts_input as sdfi
import pofah.util.event_sample as evsa
import anpofah.sample_analysis.sample_analysis as saan
import pofah.util.sample_factory as safa


def do_all_plots(data, fig_dir, bg_vs_sig, string_suffix):

    # *****************************************
    #         constituents analysis
    # *****************************************


    saan.analyze_constituents_bg_vs_sig(data, string_suffix=string_suffix, fig_dir=fig_dir)


    # *****************************************
    #         jet feature analysis
    # *****************************************

    # jet_features = ['mJJ', 'DeltaEtaJJ', 'DeltaPhiJJ', 'j1Pt', 'j2Pt', 'j1Eta']
    jet_features = ['mJJ', 'DeltaEtaJJ', 'DeltaPhiJJ', 'j1Pt', 'j2Pt']

    for feature in jet_features:
        saan.analyze_feature(data, feature, plot_name=feature+'_'+bg_id, fig_dir=fig_dir, bg_vs_sig=bg_vs_sig)



if __name__ == '__main__':


    # sample ids
    sample_ids_grav_na = ['GtoWW15na','GtoWW25na', 'GtoWW35na', 'GtoWW45na']
    sample_ids_grav_br = ['GtoWW15br','GtoWW25br', 'GtoWW35br', 'GtoWW45br']
    #sample_ids_azzz = ['AtoHZ15', 'AtoHZ20', 'AtoHZ25', 'AtoHZ30', 'AtoHZ35', 'AtoHZ40', 'AtoHZ45']
    sample_ids_qcd = ['qcdSide', 'qcdSideExt', 'qcdSig', 'qcdSigExt']
    sample_ids_all = sample_ids_qcd + sample_ids_grav

    # output paths
    fig_dir = 'fig/thesis/sample_analysis'
    print('plotting to '+ fig_dir)

    # read in all samples
    paths = safa.SamplePathDirFactory(sdfi.path_dict)


    # *****************************************
    #         read in data
    # *****************************************

    read_n = int(1e4)
    # read gravitons into sample dictionary
    data = safa.read_inputs_to_event_sample_dict_from_dir(sample_ids_grav_na, paths, read_n=read_n) # , mJJ=1200.
    # merge main and ext data for qcd
    qcd_side = evsa.EventSample.from_input_dir('qcdSide', paths.sample_dir_path('qcdSide'), read_n=read_n) # , **cuts
    qcd_side_ext = evsa.EventSample.from_input_dir('qcdSideExt', paths.sample_dir_path('qcdSideExt'), read_n=read_n)
    qcd_sig = evsa.EventSample.from_input_dir('qcdSig', paths.sample_dir_path('qcdSig'), read_n=read_n) # , **cuts
    qcd_sig_ext = evsa.EventSample.from_input_dir('qcdSigExt', paths.sample_dir_path('qcdSigExt'), read_n=read_n)
    qcd_side_all = qcd_side.merge(qcd_side_ext, name='qcdSideAll')
    qcd_sig_all = qcd_sig.merge(qcd_sig_ext, name='qcdSigAll')
    # merge sideband and signal of qcd
    qcd_all = qcd_side_all.merge(qcd_sig_all, name='qcdAll')

    # add qcd samples to sample dictionary
    data['qcdSide'] = qcd_side_all
    data['qcdSig'] = qcd_sig_all
    data['qcdAll'] = qcd_all


    # do all plots: qcd_all vs narrow gravitons
    data_na = {k: data[k] for k in ['qcdAll']+sample_ids_grav_na}
    do_all_plots(data_na, fig_dir, bg_vs_sig=True, 'qcdAll_vs_gravNa')

    # do all plots: qcd_all vs broad gravitons
    data_br = {k: data[k] for k in ['qcdAll']+sample_ids_grav_br}
    do_all_plots(data_br, fig_dir, bg_vs_sig=True, 'qcdAll_vs_gravBr')

    # do all plots: qcd_sb vs qcd_sr
    data_qcd = {k: data[k] for k in ['qcdSide', 'qcdSig']}
    do_all_plots(data_qcd, fig_dir, bg_vs_sig=False, 'qcdSide_vs_qcdSig')

    

