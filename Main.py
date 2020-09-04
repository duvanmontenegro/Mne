from bdfv4 import BdfA
import numpy as np
import mne
import os
# # Lectura de datos del tutorial
# sample_data_folder = mne.datasets.sample.data_path()
# sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample','sample_audvis_filt-0-40_raw.fif')
# ob=BdfA(sample_data_raw_file)
# # Lectura de datos en bruto del Dataset DEAP
ob=BdfA('../s01.bdf')
# # La estructura de datos de información
# ob.infor()
# # Descripción general del análisis MEG / EEG con MNE-Python
# ob.canalizacionbasica()
# ob.preprocesamiento()
# # Analizar eventos de datos sin procesar
# ob.aednp()
# # Importación de datos de dispositivos EEG
# https://mne.tools/stable/auto_tutorials/io/plot_20_reading_eeg_data.html#sphx-glr-auto-tutorials-io-plot-20-reading-eeg-data-py
# Lectura de ubicaciones de electrodos y formas de cabeza para registros de EEG 
# # Cargando datos continuos
# https://mne.tools/stable/auto_tutorials/raw/plot_10_raw_overview.html#sphx-glr-auto-tutorials-raw-plot-10-raw-overview-py
# De forma predeterminada, la familia de funciones no cargará los datos en la memoria
# en cambio, los datos en el disco se asignan en la memoria , lo que significa que los datos solo se leen del disco según sea necesario
# mne.io.read_raw_*preload=Trueread_raw_fif()load_data()crop()Raw
# Consultando el objeto Raw,Tiempo, número de muestra e índice de muestra, Modificar Rawobjetos,Seleccionar, eliminar y reordenar canales
# Cambiar el nombre y el tipo de canal
# # Trabajando con eventos
# https://mne.tools/stable/auto_tutorials/raw/plot_20_event_arrays.html#sphx-glr-auto-tutorials-raw-plot-20-event-arrays-py
# ob.teventos()
# # Métodos de trazado integrados para objetos Raw
ob.plots()
# # Descripción general de la detección de artefactos
# https://mne.tools/stable/auto_tutorials/preprocessing/plot_10_preprocessing_overview.html#sphx-glr-auto-tutorials-preprocessing-plot-10-preprocessing-overview-py
# ob.artefactos()
# # Filtrado y remuestreo de datos
# https://mne.tools/stable/auto_tutorials/preprocessing/plot_30_filtering_resampling.html#sphx-glr-auto-tutorials-preprocessing-plot-30-filtering-resampling-py
# ob.filtradore()
# # Clasificación de la etapa del sueño a partir de datos de polisomnografía (PSG)
# # Este primero es con Archivo de la guia
# ob.clasificacionP()
# # Clasificacion 
# ob.clasificacion()
