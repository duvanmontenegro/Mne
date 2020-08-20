#Librerias
# import os
import numpy as np
import mne
# from mne.datasets import sample

#Carga
raw = mne.io.read_raw_bdf("OpenBCI-BDF-2019-02-16_19-50-38.bdf", preload=True)

#Consulta informacion
print(raw)
print(raw.info)
print("Canales1: ",raw.ch_names)

#Filtrar canales por tipo o manualmente
# print(mne.pick_channels(raw.ch_names, include=['Fp1', 'AF3']))
# print(mne.pick_channels(raw.ch_names, include=[],exclude=['Fp1', 'AF3']))
print("Todo:",mne.pick_types(raw.info))
print()
print("EEG:",mne.pick_types(raw.info, meg=False, eeg=True, exclude=[]))
print()
print("MEG:",mne.pick_types(raw.info, meg=True, eeg=False, exclude=[]))
print()
print(mne.channel_type(raw.info, 0)) #ver el tipo

# Obtener lista de canales e index
# chs = raw.ch_names
# chan_idxs = [raw.ch_names.index(ch) for ch in chs]
# print(chan_idxs)
# raw.plot(order=chan_idxs, start=12, duration=4,title="Plot Uno");

#Graficas
#Imprimir señales originales en el tiempo
raw.plot(title="Plot Uno");
#Imprimir PSD de señal original
raw.plot_psd(fmax=100);

#Imprimir graficas de señales filtradas por tipo
seeg=mne.pick_types(raw.info, meg=False, eeg=True, exclude=[])
raw.plot(order=seeg, title="Plot dos");
raw.plot_psd(fmax=100);





#Pre-procesamiento
# ica = mne.preprocessing.ICA(n_components=20, random_state=0)
# ica.fit(raw.copy().filter(0, 2))

# orig_raw = raw.copy()
# raw.load_data()
# ica.apply(raw)

# events = mne.find_events(raw, stim_channel='EEG 1')
# print(events[:4]) 

# event_dict = {'auditory/left': 1, 'auditory/right': 2, 'visual/left': 3,'visual/right': 4, 'smiley': 5, 'buttonpress': 32}
# fig = mne.viz.plot_events(events, event_id=event_dict, sfreq=raw.info['sfreq'], first_samp=raw.first_samp)

# reject_criteria = dict(mag=4000e-15,grad=4000e-13,eeg=150e-6,eog=250e-6)       
# epochs = mne.Epochs(raw, events, event_id=event_dict, tmin=-0.2, tmax=0.5,reject=reject_criteria, preload=True)

# conds_we_care_about = ['auditory/left', 'auditory/right','visual/left', 'visual/right']
# epochs.equalize_event_counts(conds_we_care_about)  # this operates in-place
# aud_epochs = epochs['auditory']
# vis_epochs = epochs['visual']
# del raw, epochs  # free up memory

# aud_epochs.plot_image(picks=['F7', 'F3'])