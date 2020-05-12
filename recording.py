# -*- coding: utf-8 -*-
"""
Created on Mon May  4 20:44:23 2020

@author: Franco
"""


import pyaudio 
import wave

format = pyaudio.paInt16
 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format = pyaudio.paInt16, channels=1,
                rate = 44100, input=True,
                frames_per_buffer=1024)
print("recording...")
frames = []
 
for i in range(0, int(RATE  / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("finished recording")
 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()