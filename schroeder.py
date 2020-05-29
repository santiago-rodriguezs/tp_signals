import numpy as np
import time

def schroeder(impulse, t, fs):
    '''
    Calculates the Schroeder integral for a numpy array (input signal) using
    the numpy library. The upper limit should be calculated ideally using the 
    Lundeby method.
    
    Parameters
    ----------
    impulse : ndarray
        Impulse response signal.
    t : float, int
        Upper integration limit.
    fs : int
        Sampling frequency.

    Returns
    -------
    integrate_sch : ndarray
        Numpy array containing the Schroeder Integral of the input signal.

    '''
    short_impulse = impulse[0:round(t*fs)]
    integrate_sch = np.cumsum(short_impulse[::-1])/np.sum(impulse)

    return integrate_sch[::-1]

#------------------------------------TEST------------------------------------#

# import soundfile as sf
# import matplotlib.pyplot as plt
# from funciones.process import smoothing, logNorm, filtr

# audio, fs = sf.read('Mono.wav')
# filtered = filtr(audio, fs)
# impulse1kHz = filtered[5]
# impulse1kHz = impulse1kHz/(max(abs(impulse1kHz)))
# impulseNorm = logNorm(impulse1kHz)
# hilbert = smoothing(impulse1kHz, fs)
# hilbertNorm = logNorm(hilbert)
# median = smoothing(hilbert, fs, method = 'median')
# medianNorm = logNorm(median)

# vectorT = np.arange(len(impulse1kHz))/fs
# fs = 44100
# sch_t = 1.25
# schroeder = schroeder(median, sch_t, fs)
# schroederNorm = 10*np.log(schroeder)
# sch_vectorT = vectorT[0:round(sch_t*fs)]


# # PLOT SUAVIZADO
# plt.plot(vectorT, impulse1kHz)
# # plt.plot(vectorT, hilbert)
# plt.plot(vectorT, median, 'g')
# plt.plot(sch_vectorT, schroeder, 'r')
# plt.legend(('Impulso', 'Hilbert', 'Schroeder'))
# plt.xlim(0,1)
# plt.xlabel('Tiempo [segundos]')
# plt.ylabel('Amplitud')
# plt.title('Suavizado del impulso')
# # plt.ylim(-100, 0)

# # PLOT SUAVIZADO EN DB
# plt.plot(vectorT, impulseNorm)
# # plt.plot(vectorT, hilbert)
# plt.plot(vectorT, medianNorm, 'g')
# plt.plot(sch_vectorT, schroederNorm, 'r')
# plt.legend(('Impulso', 'Hilbert', 'Schroeder'))
# plt.xlabel('Tiempo [segundos]')
# plt.ylabel('Amplitud')
# plt.title('Suavizado del impulso en dB')
# plt.xlim(0,2)
# plt.ylim(-100, 0)
