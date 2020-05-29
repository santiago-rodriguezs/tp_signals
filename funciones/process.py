import numpy as np
from scipy.signal import iirfilter, sosfreqz, sosfilt
import matplotlib.pyplot as plt

def filtr(audio, fs, bandwidth = 'octave'):
    '''
    Filters an ndarray numpy object `audio` with an `sos` digital bandpass
    filter, for a given sampling frequency `fs`, and returns a list with each
    band octave or one-third octave filtered audio.
    
    .. note:: the octaves and third octaves will only reach 8kHz.
    
    Parameters
    ----------
    audio : ndarray
        Time value, it determines the duration of the pink noise in seconds.
    fs : int
        The sample rate of the audio data.
    bandwidth: str, optional.
        Type 'octave' for an octave band filter or typr 'third' for a 
        third-octave band filter. The default value is set to 'octave'.
    
    Example
    -------
    Import a .wav and apply an octave-band filtering.
    
        import numpy as np
        from scipy.signal import iirfilter, sosfreqz, sosfilt
        import soundfile as sf
                
        audio, fs = sf.read('example.wav')
        filtered_audio = filtr (audio, fs, bandwidth = 'octave')
        
    '''          
    user_fs = fs    
    
    if bandwidth == 'octave':
        freqs_octave = [31.25, 62.5, 125, 250, 500, 1000, 2000, 4000, 8000]
        bands_octave = []
        filtaudio_octave = []


        for fc in freqs_octave:
            
            sos = iirfilter(7, [fc / (2**(1/2)), fc * (2**(1/2))],
                            rs=60, btype='band', analog=False,
                            ftype='butter', fs=user_fs, output='sos')
            bands_octave.append(sos)
            filtaudio_octave.append(sosfilt(sos, audio))
               
        return filtaudio_octave
        
            
    elif bandwidth == 'third':
        freqs_third = [19.69, 24.80, 31.25, 39.37, 49.61, 62.50, 78.75, 99.21,
                    125, 157.5, 198.4, 250, 315, 396.9, 500, 630, 793.7, 1000,
                    1260, 1587, 2000, 2520, 3175, 4000, 5040, 6350, 8000]
        bands_third = []
        filtaudio_third =[]


        for fc in freqs_third:
            
            sos = iirfilter(7, [fc / (2**(1/6)), fc * (2**(1/6))],
                            rs=60, btype='band', analog=False,
                            ftype='butter', fs=user_fs, output='sos') 
            bands_third.append(sos)
            filtaudio_third.append(sosfilt(sos, audio))
            
        return filtaudio_third

def logNorm(audio):
    '''This function takes an audio input and returns it converted to a logarithmic scale'''
    if 0 in audio:
        minimum = min(i for i in audio if i > 0)

        audio[audio == 0] = minimum
            

    logNorm = 10 * np.log10((audio/max(audio))**2) 
   
    return logNorm

from scipy.signal import hilbert, savgol_filter, medfilt

def smoothing(audio ,fs, method = 'hilbert', window_len = 7, polyorder = 2):
    '''
    Docstring goes Here.
    '''
    if method == 'hilbert':
        smooth_audio = np.abs(hilbert(audio))
        
    if method == 'median':
        smooth_audio = medfilt(audio, window_len)
  
    if method == 'savgol':
        smooth_audio = savgol_filter(audio, window_len, polyorder)

    return smooth_audio
