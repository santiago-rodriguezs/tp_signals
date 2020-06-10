import numpy as np
import sounddevice as sd

def playrec(audio, fs):
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
    return record    


#------------------------------------TEST------------------------------------#

# import numpy as np    
# import soundfile as sf
# sineSweep, fs = sf.read('sineSweep.wav')
# record = playrec(sineSweep, fs)
# record = record/max(abs(record))
# sf.write('record_sineSweep.wav', record, fs)