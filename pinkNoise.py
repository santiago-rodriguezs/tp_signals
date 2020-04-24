import numpy as np
from scipy import signal
import soundfile as sf
import sounddevice as sd

def pinkNoise(t):
    fs = 44100
    nx = t*fs

    B = np.array([0.049922035, -0.095993537, 0.050612699, -0.004408786])
    A = np.array([1, -2.494956002, 2.017265875, -0.522189400])

    nt60 = int(np.round(np.log(1000)/1-max(np.abs(np.roots(A)))))

    v = np.random.randn(nx + nt60)
    x = signal.lfilter(B, A, v, axis = 0)

    pinkNoise = x[nt60:len(x)]

    sf.write("pinkNoise.wav", pinkNoise, fs)
    

