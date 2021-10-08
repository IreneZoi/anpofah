import pofah.path_constants.sample_dict_file_parts_input as sdfi
import pofah.util.event_sample as evsa



if __name__ == '__main__':


    # sample ids
    sample_ids_grav = ['GtoWW15na','GtoWW15br','GtoWW25na','GtoWW25br','GtoWW35na','GtoWW35br','GtoWW45na','GtoWW45br',]
    #sample_ids_azzz = ['AtoHZ15', 'AtoHZ20', 'AtoHZ25', 'AtoHZ30', 'AtoHZ35', 'AtoHZ40', 'AtoHZ45']
    sample_ids_qcd = ['qcdSide', 'qcdSideExt', 'qcdSig', 'qcdSigExt']
    sample_ids_all = sample_ids_qcd + sample_ids_grav

    # output paths
    fig_dir = 'fig/thesis/sample_analysis'
    print('plotting to '+ fig_dir)

    # read in all samples
    paths = sf.SamplePathDirFactory(sdfi.path_dict)


    # *****************************************
    #         constituents analysis
    # *****************************************

    # read gravitons
    data = sf.read_inputs_to_event_sample_dict_from_dir(sample_ids_grav, paths) # , mJJ=1200.
    # merge main and ext data for qcd
    read_n = int(1e5)
    qcd_side = evsa.EventSample.from_input_dir('qcdSide', paths.sample_dir_path('qcdSide'), read_n=read_n) # , **cuts
    qcd_side_ext = evsa.EventSample.from_input_dir('qcdSideExt', paths.sample_dir_path('qcdSideExt'), read_n=read_n)
    qcd_sig = evsa.EventSample.from_input_dir('qcdSig', paths.sample_dir_path('qcdSig'), read_n=read_n) # , **cuts
    qcd_sig_ext = evsa.EventSample.from_input_dir('qcdSigExt', paths.sample_dir_path('qcdSigExt'), read_n=read_n)
    qcd_side_all = qcd_side.merge(qcd_side_ext)
    qcd_sig_all = qcd_sig.merge(qcd_sig_ext)

    # add qcd samples to data dict
    data['qcdSide'] = qcd_side_all
    data['qcdSig'] = qcd_sig_all






