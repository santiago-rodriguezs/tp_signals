import numpy as np
import soundfile as sf
import sounddevice as sd
from multiprocessing import Process

def record(fs = 44100):
    '''Interactive way of recording audio. Please call this function 
    if you want the user to input an amount of 
    time in seconds and record that exact amount.'''
    
    timeValue = int(input('Please enter the amount of time (in seconds) to record: '))
    start = input('Press Enter to start recording.')

    print('Recording...')
    
    audio = sd.rec(frames = timeValue * fs, samplerate = fs, channels = 1)
    sd.wait()
    
    print('Recorded succesfully.')
    
    file_name = str(input('Write a name for the file: '))
    sf.write(str(file_name + '.wav'), audio, fs)
    
    print('Your file was saved as ' + file_name + '.wav')
    
    return audio

num = 1

import pyaudio
import wave
from multiprocessing import Process
 
#PLAYING    
def play(filenamePlay):
    sd.play(filenamePlay)

filenamePlay = "pinkNoise.wav"
filenameRecord = "output.wav"
seconds = 5

def playRecord(filenamePlay, filenameRecord, seconds):
    if __name__ == "__main__":
        Process(target = play, args = (filenamePlay)).start()
        Process(target = record, args = (filenameRecord, seconds)).start()
        
playRecord(filenamePlay, filenameRecord, seconds)