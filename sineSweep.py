import numpy as np
from scipy import signal
import soundfile as sf
import sounddevice as sd

def sineSweep(t, f1, f2):
    w1 = 2*np.pi*f1
    w2 = 2*np.pi*f2
    
    fs = 44100
    
    nx = t*fs
    x = np.linspace(0,t,nx)
    k = (t*w1)/np.log(w2/w1)
    l = t/np.log(w2/w1)
    
    sineSweep = np.sin(k*(np.exp(x/l)-1))
    
    sf.write("sineSweep.wav", sineSweep, fs)
    sd.play(sineSweep)
    
sineSweep(5,500,3000)