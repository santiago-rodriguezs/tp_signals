import numpy as np
from scipy.fft import fft, ifft
from scipy.signal import fftconvolve
import soundfile as sf
import matplotlib.pyplot as plt

record, fs = sf.read("./KRR/static/audio/record.wav")
inv, fs = sf.read("./KRR/static/audio/invFilter.wav")

def iRObtention(y,inv):
    '''This function takes as an input the recorded logarithmic 
    sine sweep (y) and the same inverted sine sweep (inv) and it 
    returns the impulse response of the room.'''
    
    zeros = np.zeros(len(y)-len(inv))
    inv = np.hstack((inv, zeros))
    
#    Y = fft(y)
#    INV = fft(inv)
#    
#    H = Y * INV
#    h_t = ifft(H)
    
    h_t = fftconvolve(y, inv)
    
    return h_t

def logNorm(audio):
    '''
    Takes an audio input and returns it converted to a dbFS scale.
    This function is meant to be used with numpy arrays.
    
    Parameters
    ----------
    audio : ndarray
        Numpy array containing the signal.

    Returns
    -------
    logNorm : ndarray
        Returns the same signal coverted to a dbFS scale.
        
    Example
    -------
    import numpy as np
    import matplotlib.pyplot as plt
    audio = np.random.randn(48000)
    logNorm = logNorm(audio)
    plt.plot(logNorm)
    '''
    

    if 0 in audio:
        minimum = min(i for i in audio if i > 0)
        audio[audio == 0] = minimum
    
    logNorm = 10 * np.log10((audio/max(audio))**2) 
   
    return logNorm

plt.plot(iRObtention(record, inv))