import numpy as np
from scipy.fft import fft, ifft
from scipy.signal import iirfilter, sosfilt, fftconvolve
from scipy.signal import hilbert, savgol_filter, medfilt
import soundfile as sf
import matplotlib.pyplot as plt
import os 

def iRObtention(audio,inv):
    '''This function takes as an input the recorded logarithmic 
    sine sweep (y) and the same inverted sine sweep (inv) and it 
    returns the impulse response of the room.'''
    
    h_t = fftconvolve(audio, inv)
    index = np.where(abs(h_t) == max(abs(h_t)))[0][0]
    impulse = h_t[index:]
    
    return impulse

def iRSynth(t, bandwidth, fs = 44100, A_i = 1):
    '''This function takes as an input the time length in seconds as you want your 
    impulse response to be (s), the array with t60 values corresponded with the 
    bandwidth you are going to choose (T_60), the bandwith as third or octave (bandwidth), 
    the sample rate (fs) and the amplitude array (A_1) and it returns a synthetized 
    impulse response for the given parameters.'''
    
    N = t * fs
    vectorT = np.linspace(0, t, N)

    if bandwidth == "octave":

        freqs = [62.5,125, 250, 500, 1000, 2000, 4000, 8000]
        T_60 = [0.807, 0.846, 0.9, 0.9, 0.9, 0.9, 0.876, 0.709]
    
    elif bandwidth == "third":

        freqs = [62.50, 78.75, 99.21, 125, 157.5, 198.4, 250, 315, 396.9, 500, 630, 793.7, 1000,
                    1260, 1587, 2000, 2520, 3175, 4000, 5040, 6350, 8000]
        T_60 = [0.85, 0.81, 0.881, 0.849, 0.892, 0.894, 0.891, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.843, 0.803, 0.744, 0.674]

    pi = []
    iR_i = []
    
    for i in range (0, len(freqs)):
        pi.append((-np.log(10 ** -3))/ T_60[i])

        iR_i.append(A_i * np.exp(pi[i] * vectorT) * np.cos(2 * np.pi * freqs[i] * vectorT))

    iR = np.cumsum(iR_i)
    
    iR = np.flip(iR)
    
    sf.write("./static/audio/impulseResponse.wav", iR, fs)

    return iR

def filtr(audio, bandwidth = 'octave', fs = 44100):
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
        freqs_octave = [62.5, 125, 250, 500, 1000, 2000, 4000, 8000]
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
        freqs_third = [62.50, 78.75, 99.21,
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

def smoothing(audio, method = 'hilbert',fs = 44100, window_len = 7, polyorder = 2):
    '''
    Apply smoothing to a signal. The function uses numpy and scipy.signal to
    compute the analytic signal, using the Hilbert transform. Or to apply a 
    median filter or a savitzky-golay filter to a signal.
    
    Parameters
    ----------
    audio: ndarray
        Numpy array containing the input signal.
    fs: int
        The sample rate of the audio array.
    method: str, optional.
        Optional string to determine the desired smoothing method:
            + 'hilbert' for a Hilbert transform
            + 'median' to apply a median filter.
            + 'savgol' to apply a Savitzky-Golay filter.
    window_len: int
        The length of the filter window, must be a positive odd integer.
    polyorder: int
        The order of the polynomial used to fit the samples. 
        This value value must be less than window_length.
    '''
    if method == 'hilbert':
        smooth_audio = np.abs(hilbert(audio))
        
    if method == 'median':
        smooth_audio = medfilt(audio, window_len)
  
    if method == 'savgol':
        smooth_audio = savgol_filter(audio, window_len, polyorder)

    return smooth_audio

def schroeder(impulse, t, fs = 44100):
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

def edt(impulse, fs = 44100):
    '''
    Input ndarray normalized impulse response in dBFS, return Early Decay
    Time value in seconds.
    
    Parameters
    ----------
    impulse: ndarray
        Numpy array containing the impulse response signal in dBFS
    fs: int
        The sample rate of the impluse response array.
    method: str, optional.
        Optional string to determine the desired smoothing method:
            + 'hilbert' for a Hilbert transform
            + 'median' to apply a median filter.
            + 'savgol' to apply a Savitzky-Golay filter.
    window_len: int
        The length of the filter window, must be a positive odd integer.
    polyorder: int
        The order of the polynomial used to fit the samples. 
        This value value must be less than window_length.
    '''
    
    vectorT = np.arange(len(impulse))/fs 
    index_edt = np.where(((impulse <= -1) & (impulse >= -10)))
    coeff_edt = np.polyfit(vectorT[index_edt[0]],
                       impulse[index_edt[0]], 1)
    
    fit_edt = coeff_edt[0]*vectorT + coeff_edt[1]
    edt = len(fit_edt[fit_edt>=-10])/fs
    
    return edt

def t60(impulse,  method = 't30', fs = 44100):
    '''
    Input ndarray normalized impulse response in dBFS, returns the t60 value
    in seconds. Method should be chosen according to the background noise 
    level of the input signal.
    
    Parameters
    ----------
    impulse: ndarray
        Numpy array containing the impulse response signal in dBFS
    fs: int
        The sample rate of the impluse response array.
    method: str, optional.
        Optional string to determine the desired t60 method:
            + 't10' calculate from t10.
            + 't20' calculate from t20.
            + 't30' calculate from t30.
    '''
    
    vectorT = np.arange(len(impulse))/fs 
    
    if method == 't10':
        index_t10 = np.where(((impulse <= -5) & (impulse >= -15)))
        coeff_t10 = np.polyfit(vectorT[index_t10[0]], impulse[index_t10[0]], 1)
        fit_t10 = coeff_t10[0]*vectorT + coeff_t10[1]
        t10 = len(fit_t10[fit_t10>=-10])/fs
        t60 = t10*6
        
    elif method == 't20':
        index_t20 = np.where(((impulse <= -5) & (impulse >= -25)))
        coeff_t20 = np.polyfit(vectorT[index_t20[0]], impulse[index_t20[0]], 1)
        fit_t20 = coeff_t20[0]*vectorT + coeff_t20[1]
        t20 = len(fit_t20[fit_t20>=-20])/fs
        t60 = t20*3

    elif method == 't30':
        index_t30 = np.where(((impulse <= -5) & (impulse >= -35)))
        coeff_t30 = np.polyfit(vectorT[index_t30[0]], impulse[index_t30[0]], 1)
        fit_t30 = coeff_t30[0]*vectorT + coeff_t30[1]
        t30 = len(fit_t30[fit_t30>=-30])/fs
        t60 = t30*2
        
    else:
        raise ValueError('Invalid Method.')
        
    return t60
        
def d50(impulse, fs = 44100):
    '''
    Input ndarray normalized impulse response in dBFS, return d50 value.
    The function uses Numpy to integrate the impulse.
    
    Parameters
    ----------
    impulse: ndarray
        Numpy array containing the impulse response signal in dBFS
    fs: int
        The sample rate of the impluse response array.
    '''
    t = round(0.050 * fs)
    d50 = 100 * (np.sum(impulse[:t]) / np.sum(impulse))
    
    return d50

def c80(impulse, fs = 44100):
    '''
    Input ndarray normalized impulse response in dBFS, return c80 value.
    The function uses Numpy to integrate the impulse.
    
    Parameters
    ----------
    impulse: ndarray
        Numpy array containing the impulse response signal in dBFS
    fs: int
        The sample rate of the impluse response array.
    '''
    t = round(0.080 * fs)
    c80 = 10 * np.log10(np.sum(impulse[:t]) / np.sum(impulse[t:]))
    
    return c80

def plotting(impulse):
    fs = 44100
    freqs = np.fft.rfftfreq(len(impulse), 1/fs)
    fourier = np.fft.rfft(impulse)
    spectrum = np.abs(fourier)
    spectrum[0] = 0
    spectrum = logNorm(spectrum)
    
    plt.semilogx(freqs, spectrum, '#800080')
    plt.title('Spectrum analysis of the impulse response')
    plt.ylabel('Amplitud [dBFS]')
    plt.xlabel('Frequency [Hz]')
    plt.grid(True, which="both")
    plt.xlim(20,10000)
    plt.xticks([20,50,100,200,500,1000,2000,4000,8000,10000],
               ['20','50','100','500','1000','2000','4000','8000','10000'])

    plt.savefig("./static/img/impulse.png")

    plt.close()

