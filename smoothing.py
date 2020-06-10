import numpy as np
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


##---------------------------------TESTING----------------------------------##

# # AUDIO TEST
# import soundfile as sf
# audio, fs = sf.read('audio_modif.wav')
# smooth_audio = smoothing(audio, fs, 'median')
# sf.write('smooth_audio.wav', smooth_audio, fs)

# # HILBERT TEST
# from scipy.signal import chirp
# t = 5
# fs = 44100
# vectorT = np.linspace(0, t, fs*t)
# audio = 0.9 * np.sin(4*vectorT) * chirp(vectorT, 10, vectorT[-1], 20)
# smooth_audio = smoothing(audio, fs)
# vectorT = vectorT[1*fs : 4*fs]
# audio = audio[1*fs : 4*fs]
# smooth_audio = smooth_audio[1*fs : 4*fs]  

# # MEDIAN TEST
# import soundfile as sf
# audio, fs = sf.read('audio_modif.wav')
# audio = audio[5000:7000]
# audio = audio/max(abs(audio))
# t = len(audio)/fs
# vectorT = np.linspace(0, t, len(audio))
# smooth_audio = smoothing(audio, fs, method = 'median')


# # SAVGOL TEST.
# import soundfile as sf
# audio, fs = sf.read('room.wav')
# audio = audio[2000:3000]
# audio = audio/max(abs(audio))
# t = len(audio)/fs
# vectorT = np.linspace(0, t, len(audio))
# smooth_audio = smoothing(audio, fs, method = 'savgol')

# # PLOT TEST
# import matplotlib.pyplot as plt
# plt.plot(vectorT, audio)
# plt.plot(vectorT, smooth_audio, 'r')
# plt.ylim((-1,1))
# plt.xlabel('Time [seconds]')
# plt.ylabel('Amplitude')
# plt.title('Smoothing')
# plt.legend(('Input', 'Output'))