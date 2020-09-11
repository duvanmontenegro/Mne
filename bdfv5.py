import numpy as np
import mne
import matplotlib.pyplot as plt
class BdfA(object):
	def __init__(self,url):
		self.url=url
		self.raw = None
		self.iniciar()
	def iniciar(self):
		self.raw = mne.io.read_raw_bdf(self.url, preload=True)
		# self.raw.crop(0, 1200).load_data()
	def infor(self):
		print("0------")
		print(self.raw.info)
		print("1------")
		print(self.raw.info.keys())
		print("2------")
		print(self.raw.info.ch_names)
		print("3------")
		print(mne.pick_types(self.raw.info, meg=False, eeg=True, exclude=[]))
		print("4------")
		ch_idx_by_type = mne.channel_indices_by_type(self.raw.info)
		print(ch_idx_by_type)
		print("5------")
		print(ch_idx_by_type.keys())
		print("6------")
		print(ch_idx_by_type['eeg'])
		print("7------")
		picks = (0, 1, 2, 3)
		print([mne.channel_type(self.raw.info, x) for x in picks])
		print(self.raw.get_channel_types(picks=picks))
	def filtros(self):
		self.raw.plot(scalings='auto')
		mag_channels = mne.pick_types(self.raw.info, meg='mag', eeg=True)
		fig = self.raw.plot(order=mag_channels, proj=False,n_channels=len(mag_channels), remove_dc=False,scalings='auto')
		fig.subplots_adjust(top=0.9)
		fig.suptitle('Datos {}'.format("Normales"), size='xx-large',weight='bold')
		# ps = self.raw.copy().filter(l_freq=5, h_freq=50)
		ps = self.raw.filter(l_freq=5, h_freq=50)
		print(ps)
		fig = ps.plot(order=mag_channels, proj=False,n_channels=len(mag_channels), remove_dc=False,scalings='auto')
		fig.subplots_adjust(top=0.9)
		fig.suptitle('High-pass filtered at {} Hz'.format("5-50 Hz"), size='xx-large',weight='bold')
		# Ruido de la línea eléctrica
		def add_arrows(axes):
			for ax in axes:
				freqs = ax.lines[-1].get_xdata()
				psds = ax.lines[-1].get_ydata()
				for freq in (40,50):
					idx = np.searchsorted(freqs, freq)
					y = psds[(idx - 4):(idx + 5)].max()
					ax.arrow(x=freqs[idx], y=y + 18, dx=0, dy=-12, color='red',width=0.1, head_width=3, length_includes_head=True)
		fig = self.raw.plot_psd(fmax=100, average=True)
		add_arrows(fig.axes[:2])
		meg_picks = mne.pick_types(self.raw.info,meg=True, eeg=True)
		print("meg_picks")
		print(meg_picks)
		freqs = (40)
		# raw_notch = self.raw.copy().notch_filter(freqs=freqs, picks=meg_picks)
		raw_notch = self.raw.notch_filter(freqs=freqs, picks=meg_picks)
		for title, data in zip(['Un', 'Notch'], [self.raw, raw_notch]):
			fig = data.plot_psd(fmax=100, average=True)
			fig.subplots_adjust(top=0.85)
			fig.suptitle('{}filtered'.format(title), size='xx-large', weight='bold')
			add_arrows(fig.axes[:2])
		# # reducir el muestreo de la señal puede ser un útil ahorro de tiempo.
		# raw_downsampled = self.raw.copy().resample(sfreq=100)
		raw_downsampled = self.raw.copy().resample(sfreq=100)
		for data, title in zip([self.raw, raw_downsampled], ['Original', 'Downsampled']):
			fig = data.plot_psd(average=True)
			fig.subplots_adjust(top=0.9)
			fig.suptitle(title)
			plt.setp(fig.axes, xlim=(0, 300))
	def plots(self):
		# # Navegación de datos interactiva con Raw.plot()
		self.raw.plot(scalings='auto')
		# # Trazar la densidad espectral de datos continuos
		self.raw.plot_psd(average=True)
		# # Si los datos se han filtrado, las líneas discontinuas verticales indicarán automáticamente los límites del filtro.
		# # aquí hay un gráfico de unos pocos sensores
		# midline = ['Fp1', 'F7', 'FC1', 'T7', 'C3', 'CP1'] # 'MEG 0113', 'MEG 0112', 'MEG 0111', 'MEG 0122', 'MEG 0123', 'MEG 0121'
		midline = ['Fp1', 'F7', 'FC1']
		# midline = ['EEG 1', 'EEG 2', 'EEG 3']
		# midline = ['MEG 0113', 'MEG 0112', 'MEG 0111', 'MEG 0122', 'MEG 0123', 'MEG 0121'] 
		self.raw.plot_psd(picks=midline)
	def teventos(self):
		# mapping = {'EEG 1': 'eog','EEG 4': 'misc'}
		# self.raw.set_channel_types(mapping)
		self.raw.copy().pick_types(meg=False, stim=True).plot(start=3, duration=6,scalings='auto')
		events = mne.find_events(self.raw, stim_channel='Status')
		print(events[:5])  # show the first 5
		# # Subseleccionar y combinar eventos
		# events_no_button = mne.pick_events(events, exclude=1)
		# # combinar
		# merged_events = mne.merge_events(events, [1, 2, 3], 1)
		# print(np.unique(merged_events[:, -1]))
		# # Asignación de ID de eventos a descriptores de prueba 
		event_dict = {'auditory/left': 1, 'auditory/right': 2, 'visual/left': 3,'visual/right': 4, 'smiley': 5, 'None': 6, 'None2': 7}
		# # Trazar eventos
		fig = mne.viz.plot_events(events, sfreq=self.raw.info['sfreq'],first_samp=self.raw.first_samp, event_id=event_dict)
		# fig = mne.viz.plot_events(events, sfreq=self.raw.info['sfreq'],first_samp=self.raw.first_samp)
		# # Trazar eventos y datos brutos juntos
		self.raw.plot(events=events, start=5, duration=10, color='gray',event_color={1: 'r', 2: 'g', 3: 'b', 4: 'm', 5: 'y',6:'k',7:'o'},scalings='auto')
		fig.subplots_adjust(right=0.7)
		# self.raw.plot_psd(fmax=100);
		# # Hacer matrices de eventos igualmente espaciadas
		new_events = mne.make_fixed_length_events(self.raw, start=5, stop=50, duration=2.)
		print(new_events[:5])
		fig = mne.viz.plot_events(new_events, sfreq=self.raw.info['sfreq'],first_samp=self.raw.first_samp)
		self.raw.plot(events=events, start=5, duration=10, color='gray')
		fig.subplots_adjust(right=0.7)
		self.raw.plot_psd(fmax=100)
	def clasificacion(self):
		from mne.time_frequency import psd_welch
		from sklearn.ensemble import RandomForestClassifier
		from sklearn.metrics import accuracy_score
		from sklearn.metrics import confusion_matrix
		from sklearn.metrics import classification_report
		from sklearn.pipeline import make_pipeline
		from sklearn.preprocessing import FunctionTransformer
		self.raw.plot(duration=60, scalings='auto')
		mapping = {'Fp1': 'eog'}
		self.raw.set_channel_types(mapping)
		print(self.raw.info)
		self.raw.plot(duration=60, scalings='auto')
		events = mne.find_events(self.raw, stim_channel='Status')

		# event_dict = {'auditory/left': 1, 'auditory/right': 2, 'visual/left': 3,'visual/right': 4, 'smiley': 5, 'None': 6, 'None2': 7}
		event_id={'auditory/left': 1, 'auditory/right': 2, 'visual/left': 3,'visual/right': 4, 'smiley': 5}
		# mne.viz.plot_events(events, event_id=event_dict, sfreq=self.raw.info['sfreq'])
		mne.viz.plot_events(events, event_id=event_id, sfreq=self.raw.info['sfreq'])
		# mne.viz.plot_events(events, sfreq=self.raw.info['sfreq'])
		
		stage_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
		
		tmax = 30. - 1. / self.raw.info['sfreq']  # tmax in included
		
		# epochs_train = mne.Epochs(raw=self.raw, events=events, event_id=event_dict, tmin=0., tmax=tmax, baseline=None)
		epochs_train = mne.Epochs(raw=self.raw, events=events, event_id=event_id, tmin=0., tmax=tmax, baseline=None)
		# epochs_train = mne.Epochs(raw=self.raw, events=events, tmin=0., tmax=tmax, baseline=None)
		
		print(epochs_train)
		# epochs_train.plot()

		fig, ax1 = plt.subplots(ncols=1)
		print("ax1")
		print(ax1)
		# iterate over the subjects
		stages = sorted(event_id.keys())
		print("stages")
		print(stages)
		print()
		epochs=epochs_train
		title="PSD"
		for stage, color in zip(stages, stage_colors):
			epochs[stage].plot_psd(area_mode=None, color=color, ax=ax1, fmin=0.1, fmax=20., show=False, average=True, spatial_colors=False)
			ax1.set(title=title, xlabel='Frequency (Hz)')
		plt.show()
		# exit()
		# # Diseñar un transformador scikit-learn a partir de una función de Python
		print("Scikit-learn")
		def eeg_power_band(epochs):
			FREQ_BANDS = {"delta": [0.5, 4.5], "theta": [4.5, 8.5], "alpha": [8.5, 11.5], "sigma": [11.5, 15.5], "beta": [15.5, 30]}
			psds, freqs = psd_welch(epochs, picks='eeg', fmin=0.5, fmax=30.)
			print("psds")
			print(psds)
			print("freqs")
			print(freqs)
			# Normalize the PSDs
			psds /= np.sum(psds, axis=-1, keepdims=True)
			print("psds")
			print(psds)
			X = []
			for fmin, fmax in FREQ_BANDS.values():
				psds_band = psds[:, :, (freqs >= fmin) & (freqs < fmax)].mean(axis=-1)
				X.append(psds_band.reshape(len(psds), -1))
			print("X")
			print(X)
			return np.concatenate(X, axis=1)
		# # Flujo de trabajo de clasificación multiclase usando scikit-learn
		print(eeg_power_band)
		eeg_power_band
		print("Manual")
