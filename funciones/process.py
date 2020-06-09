import numpy as np
from scipy.fft import fft, ifft
from scipy.signal import iirfilter, sosfilt
from scipy.signal import hilbert, savgol_filter, medfilt

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

def iRSynth(t, bandwidth, T_60, fs = 44100, A_i = 1):
    '''This function takes as an input the time length in seconds as you want your 
    impulse response to be (s), the array with t60 values corresponded with the 
    bandwidth you are going to choose (T_60), the bandwith as third or octave (bandwidth), 
    the sample rate (fs) and the amplitude array (A_1) and it returns a synthetized 
    impulse response for the given parameters.'''
    
    N = t * fs
    vectorT = np.linspace(0, t, N)

    if bandwidth == "octave":
        freqs = [31.25, 62.5, 125, 250, 500, 1000, 2000, 4000, 8000]
    
    elif bandwidth == "third":
        freqs = [19.69, 24.80, 31.25, 39.37, 49.61, 62.50, 78.75, 99.21,
                    125, 157.5, 198.4, 250, 315, 396.9, 500, 630, 793.7, 1000,
                    1260, 1587, 2000, 2520, 3175, 4000, 5040, 6350, 8000]

    pi = []
    iR_i = []
    
    for i in range (0, len(freqs)):
        pi.append((-np.log(10 ** -3))/ T_60[i])

        iR_i.append(A_i * np.exp(pi[i] * vectorT) * np.cos(2 * np.pi * freqs[i] * vectorT))

    iR = np.cumsum(iR_i)

    return iR

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
