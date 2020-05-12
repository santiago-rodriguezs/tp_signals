# -*- coding: utf-8 -*-
"""
Created on Mon May  4 20:50:35 2020

@author: Franco
"""

import numpy as np
import soundfile as sf
import sounddevice as sd


fs = 44100

timeValue = int(input('Please enter the amount of time (in seconds) to record: '))
start = input('Press Enter to start recording.')

print('Recording...')
audio = sd.rec(frames = timeValue * fs, samplerate = fs, channels = 1)
sd.wait()
print('Recorded succesfully.')

sf.write('recording.wav', audio, fs)

