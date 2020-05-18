import numpy as np
import soundfile as sf
import sounddevice as sd
from multiprocessing import Process

#RECORDING

def record(filenameRecord, seconds, fs = 44100):
    print('Recording...')
    
    audio = sd.rec(seconds, samplerate = fs, channels = 1)
    
    print('Recorded succesfully.')
    
    sf.write(str(filenameRecord + '.wav'), audio, fs)
    
    print('Your file was saved as ' + filenameRecord + '.wav')
 
#PLAYING    
def play(filenamePlay, fs = 44100):
    sd.play(filenamePlay, fs)

filenamePlay = "pinkNoise.wav"
filenameRecord = "output.wav"
seconds = 5

def playRecord(filenamePlay, filenameRecord, seconds):
    if __name__ == "__main__":
        Process(target = play, args = (filenamePlay)).start()
        Process(target = record, args = (filenameRecord, seconds)).start()
        
playRecord(filenamePlay, filenameRecord, seconds)