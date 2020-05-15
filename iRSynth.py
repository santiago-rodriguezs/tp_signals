import numpy as np 

def iRSynth(t, banda, T60):
    fs = 44100
    N = t * fs
    vectorT = np.linspace(0, t, N)

    if banda == "octava":
        freqs = [125, 250, 500, 1000, 2000, 4000, 8000]
#        T60 = [1.07, 1.34, 1.39, 1.22, 1.17, 1.08, 0.76]
    
    elif banda == "tercios":
        freqs = [125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2250, 3150, 4000, 5000, 6000, 8000]
#        T60 = [1.07, 1.34, 1.39, 1.22, 1.17, 1.08, 0.76, 0.52, 1.07, 1.04, 1.09, 0.32, 0.17, 1.08, 0.761, 1.07, 1.02, 0.76]

    pi = []
    ri_i = []
    
    for i in range (0, len(fcen), i++):
        pi[i] = (-np.log(10 ** -3))/ T_60[i]

        ri_i = A_i * exp(pi[i] * t) * np.cos(2 * np.pi * freqs[i] * t)

        i += 1

    ri = np.cumsum(ri_i)

    return ri