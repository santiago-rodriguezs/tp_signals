import numpy as np
from scipy.fft import fft, ifft

def iRObtention(y,inv):
    '''This function takes as an input the recorded logarithmic 
    sine sweep (y) and the same inverted sine sweep (inv) and it 
    returns the impulse response of the room.'''
    
    inv = np.array[inv, np.zeros(len(y)-len(inv))]
    
    Y = fft(y)
    INV = fft(inv)
    
    H = Y * INV
    h_t = ifft(H)
    
    return h_t