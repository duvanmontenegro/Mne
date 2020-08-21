import numpy as np
import mne
import matplotlib.pyplot as plt
import numpy as np
class BdfA(object):
	def __init__(self,url):
		self.url=url
		self.raw = None
		self.iniciar()
	def iniciar(self):
		print("Iniciar")
		# self.raw = mne.io.read_raw_bdf(self.url, preload=True)
		self.raw = mne.io.read_raw_fif(self.url)
		self.raw.crop(0, 60).load_data()
		# print("Canales1: ",self.raw.ch_names)
	def infor(self):
		# # https://mne.tools/stable/auto_tutorials/intro/plot_30_info.html#sphx-glr-auto-tutorials-intro-plot-30-info-py
		print(self.raw.info)
		# # Consultando el Infoobjeto
		# info = mne.io.read_info(self.url)
		# print(info)
		# ValueError: file does not start with a file id tag
		# print(info.keys())
		# print(self.raw.keys()) # no funciona
		print(self.raw.info.keys())
		print()
		# print(info['ch_names'])
		print(self.raw.info.ch_names)
		# print(self.raw.info.chs)
		# print(info['chs'][0].keys())
		# # Obtención de subconjuntos de canales 
		print(mne.pick_channels(self.raw.ch_names, include=['Fp1', 'AF3']))
		print(mne.pick_channels(self.raw.ch_names, include=[],exclude=['Fp1', 'AF3']))
		print(mne.pick_types(self.raw.info, meg=False, eeg=True, exclude=[]))
		print(mne.channel_type(self.raw.info, 0))
		# print(mne.pick_types(info, meg=False, eeg=True, exclude=[]))
		# # Obtención de información sobre el tipo de canal
		print(mne.channel_type(self.raw.info, 25))
		picks = (2, 12, 22, 32)
		print([mne.channel_type(self.raw.info, x) for x in picks])
		print(self.raw.get_channel_types(picks=picks))
		# # puede obtener los índices de todos los canales de todos los tipos de canales presentes en los datos
		ch_idx_by_type = mne.channel_indices_by_type(self.raw.info)
		print(ch_idx_by_type.keys())
		print(ch_idx_by_type['eeg'])
		# # Eliminar canales de un Infoobjeto
		# print(self.raw.info.nchan)
		# eeg_indices = mne.pick_types(self.raw.info, meg=False, eeg=True)
		# print(mne.pick_info(self.raw.info, eeg_indices),nchan)
	def canalizacionbasica(self):
		print(self.raw)
		print(self.raw.info)
		print("Canales1: ",self.raw.ch_names)
		# #Filtrar canales por tipo o manualmente
		# print(mne.pick_channels(raw.ch_names, include=['Fp1', 'AF3']))
		# print(mne.pick_channels(raw.ch_names, include=[],exclude=['Fp1', 'AF3']))
		# print(mne.pick_types(raw.info, meg=False, eeg=True, exclude=[]))
		# print(mne.channel_type(raw.info, 0))
		# # Obtener lista de canales e index
		# chs = raw.ch_names
		# chan_idxs = [raw.ch_names.index(ch) for ch in chs]
		# print(chan_idxs)
		# raw.plot(order=chan_idxs, start=12, duration=4,title="Plot Uno");
		#Graficas
		#Imprimir señales originales en el tiempo
		self.raw.plot(start=12, duration=4,title="Plot Uno");
		# raw.plot(block=True);
		#Imprimir PSD de señal original
		# self.raw.plot_psd(fmax=120);
		self.raw.plot_psd(fmax=50);
		#Imprimir graficas de señales filtradas por tipo
		seeg=mne.pick_types(self.raw.info, meg=False, eeg=True, exclude=[])
		self.raw.plot(order=seeg, start=12, duration=4,title="Plot dos");
		# self.raw.plot_psd(fmax=120);
		self.raw.plot_psd(fmax=50);
	def preprocesamiento(self):
		#ICA: reparación de artefactos EOG y ECG 
		ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
		ica.fit(self.raw)
		ica.exclude = [1, 2]  # details on how we picked these are omitted here
		ica.plot_properties(self.raw, picks=ica.exclude)
	#Analizar eventos de datos sin procesar 
	def aednp(self):
		# https://mne.tools/stable/auto_tutorials/intro/plot_20_events_from_raw.html#sphx-glr-auto-tutorials-intro-plot-20-events-from-raw-py
		# Un canal de estímulo (abreviatura de "canal de estímulo") es un canal que no recibe señales de un EEG, MEG u otro sensor. En cambio, los canales STIM registran voltajes
		self.raw.copy().pick_types(meg=False, stim=True).plot(start=3, duration=6)
		# self.raw.plot_psd(fmax=120);
		self.raw.plot_psd(fmax=50);
		# Conversión de una señal de canal STIM en una matriz de eventos 
		# Si sus datos tienen eventos registrados en un canal STIM, puede convertirlos en una matriz de eventos usando mne.find_events().
		events = mne.find_events(self.raw, stim_channel='Status')
		print(events[:5])
		# Leer eventos incrustados como anotaciones 
		# testing_data_folder = mne.datasets.testing.data_path()
		# eeglab_raw_file = os.path.join('s01', 'EEGLAB')
		# eeglab_raw = mne.io.read_raw_eeglab('s01.bdf')
		# print(eeglab_raw.annotations)
	def teventos(self):
		events = mne.find_events(self.raw, stim_channel='Status')
		# # Leer y escribir eventos desde / hacia un archivo
		# events_from_file = mne.read_events(self.url, encoding="utf8")
		# assert np.array_equal(events, events_from_file[:len(events)])
		# # Subseleccionar y combinar eventos
		mne.find_events(self.raw, stim_channel='Status')
		print("---")
		# events_no_button = mne.pick_events(events, exclude=1)
		# # combinar
		# merged_events = mne.merge_events(events, [1, 2, 3], 1)
		# print(np.unique(merged_events[:, -1]))
		# # Asignación de ID de eventos a descriptores de prueba 
		# event_dict = {'auditory/left': 1, 'auditory/right': 2, 'visual/left': 3,
		#               'visual/right': 4, 'smiley': 5, 'buttonpress': 32}
		event_dict = {'buttonpress': 1}
		# # Trazar eventos
		fig = mne.viz.plot_events(events, sfreq=self.raw.info['sfreq'],first_samp=self.raw.first_samp, event_id=event_dict)
		fig.subplots_adjust(right=0.7)
		# # Trazar eventos y datos brutos juntos
		self.raw.plot(events=events, start=5, duration=10, color='gray',event_color={1: 'r'})
		# self.raw.plot_psd(fmax=120);
		self.raw.plot_psd(fmax=50);
		# # Hacer matrices de eventos igualmente espaciadas
		new_events = mne.make_fixed_length_events(self.raw, start=5, stop=50, duration=2)
	def plots(self):
		# # Navegación de datos interactiva con Raw.plot()
		self.raw.plot()
		# # Trazar la densidad espectral de datos continuos
		self.raw.plot_psd(average=True)
		# # Si los datos se han filtrado, las líneas discontinuas verticales indicarán automáticamente los límites del filtro.
		# # aquí hay un gráfico de unos pocos sensores
		# midline = ['Fp1', 'F7', 'FC1', 'T7', 'C3', 'CP1'] 'MEG 0113', 'MEG 0112', 'MEG 0111', 'MEG 0122', 'MEG 0123', 'MEG 0121'
		midline = ['MEG 0113', 'MEG 0112', 'MEG 0111', 'MEG 0122', 'MEG 0123', 'MEG 0121'] 
		self.raw.plot_psd(picks=midline)
		# # Alternativamente, puede trazar el PSD para cada sensor en sus propios ejes
		# self.raw.plot_psd_topo() #RuntimeError: No digitization points found. no esta EEG por defecto
		# self.raw.copy().pick_types(meg=False, eeg=True).plot_psd_topo() # RuntimeError: No digitization points found.
		# # Trazar ubicaciones de sensores a partir de Rawobjetos
		# self.raw.plot_sensors(ch_type='eeg') #RuntimeError: No valid channel positions found
		# # Trazar proyectores a partir de Rawobjetos
		# self.raw.plot_projs_topomap(colorbar=True) #ZeroDivisionError: division by zero
	def artefactos(self):
		# # Detección de artefactos
		ssp_projectors = self.raw.info['projs']
		self.raw.del_proj()
		# # Derivas de baja frecuencia
		mag_channels = mne.pick_types(self.raw.info, meg='mag',eeg=True)
		self.raw.plot(duration=60, order=mag_channels, n_channels=len(mag_channels),remove_dc=False)
		# # Ruido de la línea eléctrica
		fig = self.raw.plot_psd(tmax=np.inf, fmax=250, average=True)
		def add_arrows(axes):
			for ax in axes:
				freqs = ax.lines[-1].get_xdata()
				psds = ax.lines[-1].get_ydata()
				for freq in (60, 120, 180, 240):
					idx = np.searchsorted(freqs, freq)
					y = psds[(idx - 4):(idx + 5)].max()
					ax.arrow(x=freqs[idx], y=y + 18, dx=0, dy=-12, color='red',width=0.1, head_width=3, length_includes_head=True)
		add_arrows(fig.axes[:2])
		# # Artefactos de latido (ECG)
		# ecg_epochs = mne.preprocessing.create_ecg_epochs(self.raw) # ValueError: Unable to generate artificial ECG channel
		# ecg_epochs.plot_image(combine='mean')
	def filtradore(self):
		# # Antecedentes sobre el filtrado
		# Un filtro elimina o atenúa partes de una señal
		# # Reparación de artefactos filtrando
		# # Derivas lentas 
		mag_channels = mne.pick_types(self.raw.info, meg='mag', eeg=True)
		self.raw.plot(order=mag_channels, proj=False,n_channels=len(mag_channels), remove_dc=False)
		for cutoff in (0.1, 0.2):
			raw_highpass = self.raw.copy().filter(l_freq=cutoff, h_freq=None)
			fig = raw_highpass.plot(order=mag_channels, proj=False,n_channels=len(mag_channels), remove_dc=False)
			fig.subplots_adjust(top=0.9)#opcional
			fig.suptitle('High-pass filtered at {} Hz'.format(cutoff), size='xx-large',weight='bold')
			# raw_highpass.plot_psd(fmax=120);
			# raw_highpass.plot_psd(fmax=50);
		filter_params = mne.filter.create_filter(self.raw.get_data(), self.raw.info['sfreq'],l_freq=0.2, h_freq=None)
		mne.viz.plot_filter(filter_params, self.raw.info['sfreq'], flim=(0.01, 5))
		def add_arrows(axes):
		    # add some arrows at 60 Hz and its harmonics
		    for ax in axes:
		        freqs = ax.lines[-1].get_xdata()
		        psds = ax.lines[-1].get_ydata()
		        for freq in (40,50):
		            idx = np.searchsorted(freqs, freq)
		            # get ymax of a small region around the freq. of interest
		            y = psds[(idx - 4):(idx + 5)].max()
		            ax.arrow(x=freqs[idx], y=y + 18, dx=0, dy=-12, color='red',width=0.1, head_width=3, length_includes_head=True)
		fig = self.raw.plot_psd(fmax=50, average=True)
		add_arrows(fig.axes[:2])
		meg_picks = mne.pick_types(self.raw.info)  # meg=True, eeg=False are the defaults
		freqs = (60, 120, 180, 240)
		raw_notch = self.raw.copy().notch_filter(freqs=freqs, picks=meg_picks)
		for title, data in zip(['Un', 'Notch '], [self.raw, raw_notch]):
		    fig = data.plot_psd(fmax=50, average=True)
		    fig.subplots_adjust(top=0.85)
		    fig.suptitle('{}filtered'.format(title), size='xx-large', weight='bold')
		    add_arrows(fig.axes[:2])