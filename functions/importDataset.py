import soundfile as sf
import numpy as np

def readwavs(*audios):
    '''
    Import a variable number of audios in format `.wav` and returns a 
    dictionary containing each audio with data type `ndarray` from numpy.
    
    
    Parameters
    ----------
    *audio : str, variable number of inputs.
        Name of audio file `.wav` in PATH.
    
    
    Example
    -------
    Import three audios.
    
        import soundfile as sf
        import numpy as np
                
        database = readwavs()     
    '''
    database = {}
    
    for i in audios:
        database[i] = sf.read(i)
    
    return database


# #----- TEST: reading two files in one line.
    
# waves = readwavs('test1.wav','test2.wav')

# # END OF TEST