# Mne
Códigos de mne para archivos bdf 
## Instalación
**Instalación rápida y sencilla, pero poco funcional.**
```
conda install scipy matplotlib scikit-learn mayavi ipython-notebook
pip install PySurfer
pip install mne --upgrade
```
_#Si no funciona agregar:_
```
pip install mne
pip install -U scikit-learn
```
**Instalación sencilla pero más pesada, tomada de la guía mne:** https://mne.tools/dev/install/contributing.html
Comandos importantes (Nos crea un entorno en conda con todo lo necesario):
```
curl --remote-name https://raw.githubusercontent.com/mne-tools/mne-python/master/environment.yml
conda env create --file environment.yml --name mnedev
conda activate mnedev
```
_Si este nuevo entorno no funciona corremos estas dos líneas:_
```
pip uninstall -y mne
pip install mne
conda activate mnedev
```
## Código funcional de pruebas:
Este código fue tomado de la página: https://mne.tools/stable/auto_tutorials/intro/plot_10_overview.html#sphx-glr-auto-tutorials-intro-plot-10-overview-py y se realizan modificaciones para trabajar con el dataset “DEAP”
 
Comenzamos importando los módulos Python necesarios:
import numpy as np
import mne

Cargando datos: al tratarse de archivos bdf se utilizará la siguiente línea:
raw = mne.io.read_raw_bdf("s01.bdf", preload=True)
"s01.bdf": es la ruta y nombre del archivo.
preload=True: este atributo permite que precargue datos en la memoria para manipulación de datos e indexación más rápida, lo cual nos puede evitar errores como: “No se encontraron puntos de digitalización.”

Para obtener información sobre el archivo el cual se está trabajando podemos usar las siguientes líneas de trabajo:
print(raw)
print(raw.info)
print("Canales1: ",raw.ch_names) - ch_names: permite ver todos los canales

Para obtener índices de los canales
print(mne.pick_channels(raw.ch_names, include=['Fp1', 'AF3']))  : solo esos dos
print(mne.pick_channels(raw.ch_names, include=[],exclude=['Fp1', 'AF3'])) : todos menos los dos
Para obtener todos y solo los índices de canales EEG (incluidos los canales EEG "malos")
print(mne.pick_types(raw.info, meg=False, eeg=True, exclude=[]))

Para saber el tipo de canal en específico:
print(mne.channel_type(raw.info, 0))
picks = (25, 76, 77, 319)
print([mne.channel_type(info, x) for x in picks])
print(raw.get_channel_types(picks=picks))
https://mne.tools/stable/auto_tutorials/intro/plot_30_info.html#tut-info-class

Para graficar: Tomamos de ejemplo dos importantes:
Gráfico de las trazas de sensor sin procesar medida en el tiempo:
raw.plot(start=12, duration=4,title="Plot Uno");
La densidad espectral de potencia (PSD): 
“Las características PSD son probablemente las características más utilizadas para BCI, y han demostrado ser eficaces para el reconocimiento de un gran número de señales neurofisiológicas.”
raw.plot_psd(fmax=120);
fmax=120: Esta frecuencia se toma del filtro pasa baja de nuestro archivo: lowpass: 104.0 Hz y no puede ser mayor a la mitad de la frecuencia general
“Código para crear una lista de los canales de las señales y mostrar esta lista”
chs = raw.ch_names
chan_idxs = [raw.ch_names.index(ch) for ch in chs]
raw.plot(order=chan_idxs, start=12, duration=4,title="Plot Uno");
raw.plot_psd(fmax=120); 

Preprocesamiento
Filtrado:
Derivas lentas: cuando la señal es de alta frecuencia y está montada en una señal de baja frecuencia, las señales rápidas pueden mantenerse iguales pero la señal de baja frecuencia en la que está montada puede tener una deriva (aumenta o disminuye).
Esta parte del código nos permitirá hacer que las desviaciones lentas sean más visibles.
mag_channels = mne.pick_types(raw.info, meg='mag', eeg=True)
raw.plot(order=mag_channels, proj=False,n_channels=len(mag_channels), remove_dc=False)
raw.plot_psd(fmax=120);
Para el filtro pasa altas utilizaremos 3Hz
raw_highpass = raw.copy().filter(l_freq=3, h_freq=None) # trabajamos sobre una copia del objeto
fig = raw_highpass.plot(order=mag_channels, proj=False,n_channels=len(mag_channels), remove_dc=False)
fig.subplots_adjust(top=0.9)#opcional
fig.suptitle('High-pass filtered at {} Hz'.format(3), size='xx-large',weight='bold')
Para crear o utilizar los diferentes tipos de filtros solo tenemos que tener en cuenta que: l_freqy h_freqson las frecuencias por debajo y por encima de las cuales, respectivamente, filtrar los datos. Así los usos son:
l_freq < h_freq: filtro de paso de banda
l_freq > h_freq: filtro de parada de banda
l_freq no es None y h_freq es None: filtro de paso alto
l_freq es None y h_freq no es None: filtro de paso bajo
raw_highpass = raw.copy().filter(l_freq=1, h_freq=50) # filtro pasa bandas
“usando la energía del filtro FIR (Finite Impulso response) elíptico para obtener precisiones de clasificación hasta el 97.5%”
Para crear un filtro FIR o IIR, utilizamos “mne.filter.create_filter”, ejemplo: 
filter_params = mne.filter.create_filter(raw.get_data(), raw.info['sfreq'],l_freq=1, h_freq=50)
https://mne.tools/stable/generated/mne.filter.create_filter.html#mne.filter.create_filter

Obtener la potencia espectral en el espacio de la frecuencia para el ruido:
def add_arrows(axes):
	for ax in axes: # Este for es para magnetómetros, gradiómetros y EEG
		freqs = ax.lines[-1].get_xdata()
		psds = ax.lines[-1].get_ydata()
		for freq in (60, 120, 180, 240):
			idx = np.searchsorted(freqs, freq)
			y = psds[(idx - 4):(idx + 5)].max()
ax.arrow(x=freqs[idx], y=y + 18, dx=0, dy=-12, color='red',width=0.1, head_width=3, length_includes_head=True)
fig = raw.plot_psd(fmax=250, average=True)
add_arrows(fig.axes[:2])
Para obtener los datos usamos get_data y usado sin parámetros especificados, extraerá todos los datos de todos los canales, en un (n_channels, n_timepoints).
print(raw.get_data())
Si desea la matriz de tiempos
data, times = raw.get_data(return_times=True)
print(data.shape)
print(times.shape)
Para el canal (s) extracto específico y los rangos de la muestra
first_channel_data = raw.get_data(picks=0)
eeg_and_eog_data = raw.get_data(picks=['eeg', 'eog'])
two_meg_chans_data = raw.get_data(picks=['AF3', 'F7'],start=1000, stop=2000)


Técnicas de extracción de características de señales EEG en la imaginación de movimiento para sistemas BCI
Dada la modesta velocidad y precisión de un BCI basado en EEG, se hace necesario el uso tanto de sistemas multicanal como de métodos adecuados de procesado de señal. El procesado de la señal EEG se divide en varias etapas: pre-procesamiento, extracción de características, selección y clasificación de las mismas.
Técnicas de extracción utilizadas: Técnicas en el dominio del tiempo, Técnicas en dominio de la frecuencia (PSD - Power Spectral Density), 
https://www.revistaespacios.com/a18v39n22/a18v39n22p36.pdf
