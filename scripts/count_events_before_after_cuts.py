import pofah.path_constants.sample_dict_file_parts_input_dshep as sadi
import pofah.util.sample_factory as sf
import numpy as np


sample_ids = sadi.path_dict['sample_dir'].keys()
paths = sf.SamplePathDirFactory(sadi.path_dict)
data = sf.read_inputs_to_jet_sample_dict_from_dir(sample_ids, paths, apply_mjj_cut=False)

with open('./event_counts.csv', 'a', newline='\n') as ff:

	ff.write(','.join(['sample_name', 'n_total', 'n_cut_mjj_1100', 'n_cut_dEta_1.4', 'n_cut_dEta_mjj', 'min_dEta', 'max_dEta', 'min_mJJ', 'max_mJJ']) + '\n\n')

	for sample_name, events in data.items():

		# cut in mJJ and dEta
		events_mjj_cut = events.cut(events['mJJ'] > 1100.) # cut on mJJ > 1100.
		events_dEta_cut = events.cut(np.abs(events['DeltaEtaJJ']) > 1.4) # cut on |dEta| >= 1.4
		events_mjj_dEta_cut = events_mjj_cut.cut(np.abs(events_mjj_cut['DeltaEtaJJ']) > 1.4) # cut mJJ *and* dEta
		
		# count events
		n_total = len(events)
		n_cut_mjj = len(events_mjj_cut)
		n_cut_dEta = len(events_dEta_cut)
		n_cut_mjj_dEta = len(events_mjj_dEta_cut)

		with np.printoptions(precision=5, suppress=True):

			print("{: <12}: {: >7} n_total, {: >7} n_mjj_cut, {: >7} n_dEta_cut, {: >7} n_mjj_dEta_cut, {: >5} n_mjj_dEta_cut / n_total".format(sample_name, n_total, n_cut_mjj, n_cut_dEta, n_cut_mjj_dEta, n_cut_mjj_dEta/float(n_total)))

			ff.write(','.join([sample_name] + [str(n) for n in [n_total, n_cut_mjj, n_cut_dEta, n_cut_mjj_dEta, np.min(events['DeltaEtaJJ']), np.max(events['DeltaEtaJJ']), np.min(events['mJJ']), np.max(events['mJJ'])]]))
			ff.write('\n')


