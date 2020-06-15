import numpy as np

def lundeby(impulse, fs):
    pass

import soundfile as sf
import matplotlib.pyplot as plt
from funciones.process import smoothing, logNorm, filtr

#IMPORTO LA RESPUESTA AL IMPULSO Y LA HAGO MIERDA. (EN DB)
audio, fs = sf.read('Mono.wav')
vectorN = np.arange(0, len(audio))
vectorT = vectorN/fs
filtered = filtr(audio, fs)
impulse1kHz = filtered[5]/(max(abs(filtered[5])))
hilbert = smoothing(impulse1kHz, fs)
impulse = smoothing(hilbert, fs, method = 'median')
impulse = logNorm(impulse)

#CREO LA FUNCION RMS PARA DB (??????)
dBrms = lambda impulse: -1*np.sqrt(np.mean(impulse**2))

#CREO UN VECTOR CON LOS VALORES RMS DE VENTANAS DE 1ms.
vectorRMS = np.empty(0)
window = round(0.01 * fs)
for i in range(0, len(impulse), window):
    vectorRMS = np.append(vectorRMS, dBrms(impulse[i:i+window]))

#CALCULO EL VALOR DE LA COLA DE LA SENAL (ULTIMO 10%)
rms_tail = dBrms(impulse[-len(impulse)//10:])

#AJUSTO LA RECTA DESDE 0 HASTA 10DB ARRIBA DE LA COLA.
not_noise_index = np.asarray(vectorRMS > rms_tail + 10).nonzero()
not_noise_index = not_noise_index[0][-1]
coeff = np.polyfit(vectorN[:window*not_noise_index],
                        impulse[:window*not_noise_index], 1)
fit = coeff[0]*vectorN + coeff[1]
crosspoint = (rms_tail-coeff[1])/coeff[0]

#ACA EMPIEZO A ITERAR??????
precision = 1
max_tries = 50
tries = 0
plt.plot(vectorT, impulse, '')
plt.plot(vectorT, fit,'r')

while tries < max_tries:
 
    #PONGO NUEVOS INTERVALOS
    dB_interval = (-10)/coeff[0]
    n_intervals = 3
    window = int(round(dB_interval/n_intervals) )   #3 intervalos cada 10dB
    vectorRMS = np.empty(0)
    
    #CALCULO EL RMS PARA LOS NUEVOS INTERVALOS
    for i in range(0, len(impulse), window):
        vectorRMS = np.append(vectorRMS, dBrms(impulse[i:i+window]))
    
    #CALCULO EL NOISE LEVEL
    noise_index = int(round((rms_tail-10-coeff[1])/coeff[0]))
    noise_level = dBrms(impulse[noise_index:])
    
    #CALCULO LA NUEVA RECTA
    not_noise_index = np.where(((vectorRMS > noise_level+10) & 
                                (vectorRMS <= noise_level+30)))
    first_index = (not_noise_index[0]-1)[0]*window
    last_index = not_noise_index[0][-1]*window
    coeff = np.polyfit(vectorN[first_index:last_index],
                       impulse[first_index:last_index], 1)
    fit = coeff[0]*vectorN + coeff[1]
    
    precision = abs(crosspoint - (rms_tail-coeff[1])/coeff[0])/crosspoint
    crosspoint = (rms_tail-coeff[1])/coeff[0]
    tries += 1
    plt.plot(vectorT, fit)
    
# crosspoint = 


