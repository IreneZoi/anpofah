import numpy as np


def bin_data_to_image(self, events, bin_borders, bins_n):

    eta_idx, phi_idx, pt_idx = range(3)
    eventImagesShape = (events.shape[0], bins_n, bins_n)
    images = np.zeros(eventImagesShape, dtype="float32")

    for eventNo, event in enumerate(events):  # for each event (100x3) populate eta-phi binned image with pt values
        # bin eta and phi of event event
        binIdxEta = np.digitize(event[:, eta_idx], bin_borders, right=True) - 1  # np.digitize starts binning with 1
        binIdxPhi = np.digitize(event[:, phi_idx], bin_borders, right=True) - 1
        for particle in range(event.shape[0]):
            images[eventNo, binIdxEta[particle], binIdxPhi[particle]] += event[particle, pt_idx]  # add pt to bin of jet image

    return images


def convert_jet_particles_to_jet_image(particles_j1, partciles_j2, bins_n=32):
    ''' convert a dataset of jet1 and jet2 particle lists to jet images binned by dEta and dPhi '''

    minAngle = -0.8;
    maxAngle = 0.8
    bin_borders = np.linspace(minAngle, maxAngle, num=bins_n)  # bins for eta & phi

    return [bin_data_to_image(particles_j1, bin_borders, bins_n), bin_data_to_image(particles_j2, bin_borders, bins_n)]