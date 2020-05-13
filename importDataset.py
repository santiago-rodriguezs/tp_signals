import soundfile as sf
import numpy as np

def read(*args):
    '''
    Docstring goes here.
    '''
    database = {}
    
    for i in args:
        database[i] = sf.read(i)
    
    return database

waves = read('test1.wav','test2.wav')
