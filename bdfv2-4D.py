#Este tutorial cubre los conceptos básicos de la detección de artefactos e introduce las herramientas de detección de artefactos disponibles en MNE-Python.
import os
import numpy as np
import mne

raw = mne.io.read_raw_bdf("s01.bdf", preload=True)
raw.crop(0, 60).load_data() 

#Detección de artefactos 
ssp_projectors = raw.info['projs']
raw.del_proj()
#Derivas de baja frecuencia
mag_channels = mne.pick_types(raw.info, meg='mag',eeg=True)
raw.plot(duration=60, order=mag_channels, n_channels=len(mag_channels),remove_dc=False)
raw.plot_psd(fmax=120);
#Ruido de la línea de alimentación
fig = raw.plot_psd(tmax=np.inf, fmax=250, average=True)
# add some arrows at 60 Hz and its harmonics:
for ax in fig.axes[:2]:
	freqs = ax.lines[-1].get_xdata()
	psds = ax.lines[-1].get_ydata()
	for freq in (60, 120, 180, 240):
		idx = np.searchsorted(freqs, freq)
		ax.arrow(x=freqs[idx], y=psds[idx] + 18, dx=0, dy=-12, color='red',width=0.1, head_width=3, length_includes_head=True)

#Artefactos de latidos del corazón (ECG) 
#ValueError: no se puede generar un canal de ECG artificial
#https://mne.tools/stable/generated/mne.preprocessing.create_ecg_epochs.html#mne.preprocessing.create_ecg_epochs
# print(mne.pick_types(raw.info, meg=True, eeg=False, exclude=[]))
# ecg_epochs = mne.preprocessing.create_ecg_epochs(raw)
# ecg_epochs.plot_image(combine='mean')

#Artefactos oculares (EOG)
# print(mne.pick_types(raw.info, meg=False, eeg=False, eog=True))
# eog_epochs = mne.preprocessing.create_eog_epochs(raw, picks='eeg')
eog_epochs = mne.preprocessing.create_eog_epochs(raw, baseline=(-0.5, -0.2))
eog_epochs.plot_image(combine='mean')
# eog_epochs.average().plot_joint()
