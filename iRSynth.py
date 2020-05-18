import numpy as np 

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

#--------------------------------TESTING---------------------------------------
#T_60 = [1, 0.7, 1.2, 1.4, 1.12, 1.72, 1.20, 1.05, 0.70]
#
#print(iRSynth(5, "octave", T_60))