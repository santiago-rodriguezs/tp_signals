import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from funciones.process import filtr, iRObtention, smoothing, logNorm, schroeder, edt, t60, d50, c80
from funciones.callibrate import sineSweep, pinkNoise


def lundeby(impulse, fs):
    '''
    Docstring goes here.
    '''
    #CREO LA FUNCION RMS PARA DB
    dBrms = lambda impulse: -1*np.sqrt(np.mean(impulse**2))
    
    #CREO UN VECTOR CON LOS VALORES RMS DE VENTANAS DE 1ms.
    vectorRMS = np.empty(0)
    window = round(0.01 * fs)
    for i in range(0, len(smooth_impulse), window):
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
    
    #ACA EMPIEZO A ITERAR
    precision = 1
    max_tries = 50
    tries = 0
    plt.plot(vectorT, impulse, 'y')
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
        if noise_index > len(vectorN):
            noise_level = dBrms(impulse[-len(impulse)//10:])
        else:
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
        
    return crosspoint/fs


    



#------------------------------------TEST------------------------------------#

# IMPORTO LA RESPUESTA LA GRABACION Y LA CONVOLUCIONO.
record, fs = sf.read('record.wav')
inv, fs = sf.read('invFilter.wav')
impulse = iRObtention(record, inv)
filtered_list = filtr(impulse)
impulse_1kHz = filtered_list[5]
smooth_impulse = smoothing(impulse_1kHz, "hilbert")
smooth_impulse = smoothing(smooth_impulse, "median")
smooth_impulse = smoothing(smooth_impulse, "savgol")
impulse = logNorm(impulse_1kHz)

vectorN = np.arange(0, len(impulse))
vectorT = np.arange(0, len(impulse))/fs

crosspoint = lundeby(impulse, fs)

