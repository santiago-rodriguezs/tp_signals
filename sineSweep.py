import numpy as np
import soundfile as sf
import sounddevice as sd

def sineSweep(t, f1, f2, inv = False):
    '''Esto Esto un docstring del SineSweep.'''
    w1 = 2*np.pi*f1
    w2 = 2*np.pi*f2
    
    fs = 44100
    
    nx = t*fs
    vectorT = np.linspace(0,t,nx)
    k = (t*w1)/np.log(w2/w1)
    l = t/np.log(w2/w1)
  
    if inv == False:
        sineSweep = 0.5*np.sin(k*(np.exp(vectorT/l)-1))
        sf.write("sineSweep.wav", sineSweep, fs)
        return sineSweep
    
    elif inv == True: 
        w = k/l * np.exp(vectorT/l)
        m = w1/(2*np.pi*w)
        vectorT = -vectorT
        sineSweep = 0.5*np.sin(k*(np.exp(vectorT/l)-1))
        invFilter = m * sineSweep  
        sf.write("invFilter.wav", invFilter, fs)
        return invFilter 
    
    else:
        return 'Invalid Argument.'
    
    
    
    



    
