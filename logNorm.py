import numpy as np

def logNorm(audio):
    '''This function takes an audio input and returns it converted to a logarithmic scale'''
    if 0 in audio:
        minimum = min(i for i in audio if i > 0)

        audio[audio == 0] = minimum
            

    logNorm = 20 * np.log10(audio/max(audio)) 
   
    return logNorm

    







