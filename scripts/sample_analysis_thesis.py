import pofah.path_constants.sample_dict_file_parts_input as sdfi




if __name__ == '__main__':


    # sample ids
    sample_ids_grav = ['GtoWW15na','GtoWW15br','GtoWW25na','GtoWW25br','GtoWW35na','GtoWW35br','GtoWW45na','GtoWW45br',]
    #sample_ids_azzz = ['AtoHZ15', 'AtoHZ20', 'AtoHZ25', 'AtoHZ30', 'AtoHZ35', 'AtoHZ40', 'AtoHZ45']
    sample_ids_qcd = ['qcdSide', 'qcdSideExt', 'qcdSig', 'qcdSigExt']

    # output paths
    fig_dir = 'fig/thesis/sample_analysis'
    print('plotting to '+ fig_dir)

    # read in all samples
    paths = sf.SamplePathDirFactory(sdfi.path_dict)


