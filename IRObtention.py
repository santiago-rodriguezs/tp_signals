import numpy as np
from scipy.fft import fft, ifft

def iRObtention(y,inv):
    inv = np.array[inv, np.zeros(len(y)-len(inv))]
    
    Y = fft(y)
    INV = fft(inv)
    
    H = Y * INV
    h_t = ifft(H)
    
    return h_t