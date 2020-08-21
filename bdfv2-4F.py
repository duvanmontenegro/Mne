#Este tutorial cubre el filtrado y el remuestreo, y brinda ejemplos de cómo se puede utilizar el filtrado para la reparación de artefactos.
import os
import numpy as np
import matplotlib.pyplot as plt
import mne


raw = mne.io.read_raw_bdf("../s01.bdf", preload=True)
# raw = mne.io.read_raw_bdf("OpenBCI-BDF-2019-02-16_19-50-38.bdf", preload=True)
print(raw.info)
print(raw.info['sfreq'])
print(raw.get_data())
data = raw.get_data()
print(data.shape)
#solo mostramos 60s para ahorrar memoria
raw.crop(0, 60).load_data() 

#Derivas lentas
mag_channels = mne.pick_types(raw.info, meg='mag', eeg=True)
# raw.plot(duration=60, order=mag_channels, proj=False,n_channels=len(mag_channels), remove_dc=False)
raw.plot(order=mag_channels, proj=False,n_channels=len(mag_channels), remove_dc=False)
# raw.plot_psd(fmax=120);
# raw.plot_psd(fmax=100);

# paso alto
# for cutoff in (0.1, 0.2):
# 	raw_highpass = raw.copy().filter(l_freq=cutoff, h_freq=None)
# 	# fig = raw_highpass.plot(duration=60, order=mag_channels, proj=False,n_channels=len(mag_channels), remove_dc=False)
# 	fig = raw_highpass.plot(order=mag_channels, proj=False,n_channels=len(mag_channels), remove_dc=False)
# 	fig.subplots_adjust(top=0.9)#opcional
# 	fig.suptitle('High-pass filtered at {} Hz'.format(cutoff), size='xx-large',weight='bold')
# 	raw_highpass.plot_psd(fmax=120);
# 	# raw_highpass.plot_psd(fmax=100);
# raw_highpass = raw.copy().filter(l_freq=1, h_freq=50)
raw_highpass = raw.copy().filter(l_freq=3, h_freq=None)
fig = raw_highpass.plot(order=mag_channels, proj=False,n_channels=len(mag_channels), remove_dc=False)
fig.subplots_adjust(top=0.9)#opcional
fig.suptitle('High-pass filtered at {} Hz'.format(3), size='xx-large',weight='bold')
# raw_highpass.plot_psd(fmax=120);
print("los datos sin filtro")
data = raw.get_data()
print(data.shape)

data, times = raw.get_data(return_times=True)
print(data.shape)
print(times.shape)

first_channel_data = raw.get_data(picks=0)
eeg_and_eog_data = raw.get_data(picks=['eeg', 'eog'])
two_meg_chans_data = raw.get_data(picks=['AF3', 'F7'],start=1000, stop=2000)

print(first_channel_data.shape)
print(eeg_and_eog_data.shape)
print(two_meg_chans_data.shape)

print("los datos con filtro")
print(raw_highpass.get_data())

# Si 0.1 Hz no fue lo suficientemente alto como para eliminar por completo las derivas lentas.
filter_params = mne.filter.create_filter(raw.get_data(), raw.info['sfreq'],l_freq=0.2, h_freq=None)

# Ahora puede pasar los parámetros del filtro
mne.viz.plot_filter(filter_params, raw.info['sfreq'], flim=(0.01, 5))

# Ruido de la línea de alimentación

def add_arrows(axes):
	for ax in axes:
		freqs = ax.lines[-1].get_xdata()
		psds = ax.lines[-1].get_ydata()
		for freq in (60, 120, 180, 240):
			idx = np.searchsorted(freqs, freq)
			y = psds[(idx - 4):(idx + 5)].max()
			ax.arrow(x=freqs[idx], y=y + 18, dx=0, dy=-12, color='red',width=0.1, head_width=3, length_includes_head=True)
fig = raw.plot_psd(fmax=250, average=True)
# fig = raw.plot_psd(fmax=100, average=True)
add_arrows(fig.axes[:2])

#Debería ser evidente que los canales MEG son más susceptibles a este tipo de interferencia que el EEG
#unfiltered,notch unfiltered(sin filtro-muesca sin filtrar)
# notch_filter()también tiene parámetros para controlar el ancho de muesca, el ancho de banda de transición y otros aspectos del filtro. Vea la cadena de documentación para más detalles.
meg_picks = mne.pick_types(raw.info,meg=True, eeg=True)  # meg=True, eeg=False are the defaults
freqs = (60, 120, 180, 240)
raw_notch = raw.copy().notch_filter(freqs=freqs, picks=meg_picks)
for title, data in zip(['Un', 'Notch'], [raw, raw_notch]):
	fig = data.plot_psd(fmax=250, average=True)
	# fig = data.plot_psd(fmax=100, average=True)
	fig.subplots_adjust(top=0.85)
	fig.suptitle('{}filtered'.format(title), size='xx-large', weight='bold')
	add_arrows(fig.axes[:2])

#Remuestreo
#Submuestreado
raw_downsampled = raw.copy().resample(sfreq=200)
for data, title in zip([raw, raw_downsampled], ['Original', 'Downsampled']):
	fig = data.plot_psd(average=True)
	fig.subplots_adjust(top=0.9)
	fig.suptitle(title)
	plt.setp(fig.axes, xlim=(0, 300))

#Mejores prácticas 
print("Mejores prácticas")

current_sfreq = raw.info['sfreq']
desired_sfreq = 56.888888888888886 # Hz
decim = np.round(current_sfreq / desired_sfreq).astype(int)
obtained_sfreq = current_sfreq / decim
lowpass_freq = obtained_sfreq / 3.

raw_filtered = raw.copy().filter(l_freq=None, h_freq=lowpass_freq)
events = mne.find_events(raw_filtered)
epochs = mne.Epochs(raw_filtered, events, decim=decim)

# raw_filtered.plot(duration=60, proj=False, remove_dc=False)
raw_filtered.plot(proj=False, remove_dc=False)
raw_filtered.plot_psd();

print('desired sampling frequency was {} Hz; decim factor of {} yielded an ''actual sampling frequency of {} Hz.'.format(desired_sfreq, decim, epochs.info['sfreq']))