import numpy as np

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
            

    logNorm = 20 * np.log10((audio/max(audio))**2) 
   
    return logNorm








