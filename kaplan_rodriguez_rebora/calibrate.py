import numpy as np
import soundfile as sf
from scipy.signal import lfilter
import sounddevice as sd

def sineSweep(t, f1, f2, inv = False, fs = 44100):
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
    
    nx = round(t*fs)
    vectorT = np.linspace(0,t,nx)
    k = (t*w1)/np.log(w2/w1)
    l = t/np.log(w2/w1)
    sineSweep = np.sin(k*(np.exp(vectorT/l)-1))

  
    if inv == False:
        sf.write("./static/audio/sineSweep.wav", sineSweep, fs)
        return sineSweep
    
    elif inv == True: 
        w = (k/l) * np.exp(vectorT/l)
        m = w1/(2*np.pi*w)
        invFilter = m * np.flip(sineSweep)
        invFilter = invFilter/max(abs(invFilter))
        sf.write("./static/audio/invFilter.wav", invFilter, fs)
        return invFilter 
    
    else:
        return 'Invalid Argument.'

def pinkNoise(t, fs = 44100):
    '''
    Creates pink noise for a given time `t` in seconds, using the numpy,
    scipy and soundfile libraries.
    
    .. note:: If `pinkNoise.wav` exists, it will be overwritten.
    
    Parameters
    ----------
    t : int
        Time value, it determines the duration of the pink noise in seconds.
    fs : int
        The sample rate of the audio data. The default value is set to 44100Hz.
    
    Example
    -------
    Write a `.wav` from a numpy array containing ten seconds of
    pink noise with a given samplerate.
    
        import numpy as np
        import soundfile as sf
        from scipy import signal
        
        pinkNoise(10)
    '''
    
    nx = t*fs

    B = np.array([0.049922035, -0.095993537, 0.050612699, -0.004408786])
    A = np.array([1, -2.494956002, 2.017265875, -0.522189400])

    nt60 = int(np.round(np.log(1000)/1-max(np.abs(np.roots(A)))))

    v = np.random.randn(nx + nt60)
    x = lfilter(B, A, v, axis = 0)

    pinkNoise = x[nt60:len(x)]

    sf.write("./static/audio/pinkNoise.wav", pinkNoise, fs)
    
    return pinkNoise

def playRec(audio, fs = 44100):
    '''
    Plays an audio input and simultaneously records the default microphone 
    through your default system audio drivers, using the Sounddevice library.
    
    Parameters
    ----------
    audio : ndarray
        Numpy array containing the input signal.
    fs : int
        Sampling frequency.

    Returns
    -------
    record : ndarray
        Numpy array containing the mono normalized signal recorded from the
        micrpohone.

    '''
    
    record = sd.playrec(audio, samplerate = fs, channels = 1)
    sd.wait()
    record = record/max(abs(record))
    sf.write("./static/audio/record.wav", record, fs)
    return record    
