import pofah.path_constants.sample_dict_file_parts_input as sdfi
import pofah.util.event_sample as evsa
import anpofah.sample_analysis.sample_analysis as saan
import pofah.util.sample_factory as safa



if __name__ == '__main__':


    # sample ids
    sample_ids_grav_na = ['GtoWW15na','GtoWW25na']
    sample_ids_grav = ['GtoWW15na','GtoWW15br','GtoWW25na','GtoWW25br','GtoWW35na','GtoWW35br','GtoWW45na','GtoWW45br',]
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

    read_n = int(1e3)
    # read gravitons into sample dictionary
    data = safa.read_inputs_to_event_sample_dict_from_dir(sample_ids_grav_na, paths, read_n=read_n) # , mJJ=1200.
    # merge main and ext data for qcd
    qcd_side = evsa.EventSample.from_input_dir('qcdSide', paths.sample_dir_path('qcdSide'), read_n=read_n) # , **cuts
    qcd_side_ext = evsa.EventSample.from_input_dir('qcdSideExt', paths.sample_dir_path('qcdSideExt'), read_n=read_n)
    # qcd_sig = evsa.EventSample.from_input_dir('qcdSig', paths.sample_dir_path('qcdSig'), read_n=read_n) # , **cuts
    # qcd_sig_ext = evsa.EventSample.from_input_dir('qcdSigExt', paths.sample_dir_path('qcdSigExt'), read_n=read_n)
    qcd_side_all = qcd_side.merge(qcd_side_ext, name='qcdSideAll')
    # qcd_sig_all = qcd_sig.merge(qcd_sig_ext, name='qcdSigAll')

    # add qcd samples to sample dictionary
    data['qcdSide'] = qcd_side_all
    # data['qcdSig'] = qcd_sig_all

    bg_id = 'qcdSide'

    # *****************************************
    #         constituents analysis
    # *****************************************


    saan.analyze_constituents_bg_vs_sig(data, fig_dir=fig_dir)


    # *****************************************
    #         jet feature analysis
    # *****************************************

    # jet_features = ['mJJ', 'DeltaEtaJJ', 'DeltaPhiJJ', 'j1Pt', 'j2Pt', 'j1Eta']
    jet_features = ['mJJ', 'DeltaEtaJJ', 'DeltaPhiJJ', 'j1Pt', 'j2Pt']

    for feature in jet_features:
        saan.analyze_feature(data, feature, plot_name=feature+'_'+bg_id, fig_dir=fig_dir, bg_vs_sig=True)

