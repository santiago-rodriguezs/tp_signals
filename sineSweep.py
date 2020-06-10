import numpy as np
import soundfile as sf

def sineSweep(t, f1, f2, inv = False):
    '''
    Create a sine sweep between two frequencies with a duration of `t`
    seconds. If the inv parameter is True, then this creates the same 
    sine sweep and applies an inverse filter to it.
    
    .. note:: If `sineSweep` or `invFilter` exists, it will be overwritten.
    
    Parameters
    ----------
    t : float or int
        Time value, it determines the duration of the sinesweep in seconds.
    f1 : int
        Starting frequency for the sweep.
    f2 : int
        Ending frequency for the sweep.
    fs : int
        The sample rate of the audio data. The default value is set to 44100.
    inv : bool, optional
        If True, this creates a sine sweep and applies an inverse filter to it.
    
    Example
    -------
    Write a sine sweep that ranges from 20hz to 20Khz with the 
    default samplerate.
    
        import numpy as np
        import soundfile as sf
        sineSweep(10, 20, 20000)
    '''
    w1 = 2*np.pi*f1
    w2 = 2*np.pi*f2
    
    fs = 44100
    
    nx = round(t*fs)
    vectorT = np.linspace(0,t,nx)
    k = (t*w1)/np.log(w2/w1)
    l = t/np.log(w2/w1)
    sineSweep = np.sin(k*(np.exp(vectorT/l)-1))

  
    if inv == False:
        sf.write("sineSweep.wav", sineSweep, fs)
        return sineSweep
    
    elif inv == True: 
        w = (k/l) * np.exp(vectorT/l)
        m = w1/(2*np.pi*w)
        invFilter = m * np.flip(sineSweep)
        invFilter = invFilter/max(abs(invFilter))
        sf.write("invFilter.wav", invFilter, fs)
        return invFilter 
    
    else:
        return 'Invalid Argument.'