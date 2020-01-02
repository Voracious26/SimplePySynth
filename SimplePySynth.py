import numpy as np
import simpleaudio as sa
from envelope import envelope
from dial import dial
from tkinter import Tk, Canvas
import matplotlib.pyplot as plt
import threading

fs = 44100  # 44100 samples per second

def sinWave(frequency, length):
    t = np.linspace(0, length, length * fs, False)
    outputWave = np.sin(frequency * t * 2 * np.pi)
    return outputWave

def sawWave(frequency, length, n):
    t = np.linspace(0, length, length * fs, False)
    outputWave = np.sin(frequency * t * 2 * np.pi)
    for k in range(1, n):
        harmonic = np.sin(frequency * t * k * 2 * np.pi) / k
        outputWave += harmonic
    return outputWave

def squareWave(frequency, length, n):
    t = np.linspace(0, length, length * fs, False)
    outputWave = np.sin(frequency * t * 2 * np.pi)
    for k in range(1, n):
        harmonic = np.sin(frequency * t * (1+2*k) * 2 * np.pi) / k
        outputWave += harmonic
    return outputWave

def playNote(wavetype, frequency, seconds, volume, attack, decay, sustain, release):
    length = seconds + release
    
    A = attack * fs
    B = (attack + decay) * fs
    C = seconds * fs
    D = (seconds + release) * fs

    if wavetype == "saw":
        note = sawWave(frequency, length, 8)
    elif wavetype == "square":        
        note = squareWave(frequency, length, 8)
    elif wavetype == "sin":
        note = sinWave(frequency, length)

    masterAmp = (volume/100)
    for i in range(0, note.size):
        amp = (i < A) * (i/A)
        amp += (A <= i < B) * (((sustain - 1)/(B-A))*(i - B) + sustain)
        amp += (B <= i < C) * sustain
        amp += (C <= i < D) * ((sustain/(C-D))*(i - D))
        note[i] *= amp
        note[i] *= masterAmp
        if(note[i] > 1):
            note[i] = 1
        if(note[i] < -1):
            note[i] = -1      
    # Ensure that highest value is in 16-bit range
    #audio = note * (2**15 - 1) / np.max(np.abs(note))
    audio = note * (2**15 - 1)
    # Convert to 16-bit data
    audio = audio.astype(np.int16)

    # Start playback
    play_obj = sa.play_buffer(audio, 1, 2, fs)

    # Wait for playback to finish before exiting
    play_obj.wait_done()

notes = [440, 880, 440, 220]

root = Tk()
paint = Canvas(root)  
volumeEnvelope = envelope(paint)
masterVolume = dial(paint, 350, 150, 20)

def drawEverything():
    global volumeEnvelope
    volumeEnvelope.draw()
    masterVolume.drawD()

def key(event):
    repr(event.char)
    
def callback(event):
    global volumeEnvelope
    drawEverything()
    volumeEnvelope.clickedD(event)
    masterVolume.clickedD(event)

def moving(event):
    global volumeEnvelope
    drawEverything()
    volumeEnvelope.movingD(event)
    masterVolume.movingD(event)

def released(event):
    global volumeEnvelope
    drawEverything()
    volumeEnvelope.releasedD(event)
    masterVolume.releasedD(event)

paint.bind("<Key>", key)
paint.bind("<Button-1>", callback)
paint.bind("<ButtonRelease-1>", released)
paint.bind("<B1-Motion>", moving)
paint.pack()

def GUIupdate():
    while True:
        drawEverything()
        root.update()
        
def playNotes():
    for k in range(0, 3):
        for j in notes:
            #playNote("saw", j, 1, 0.5, 0.5, 1, 0.5)
            #print(masterVolume.value/100)
            playNote("saw", j, 1, masterVolume.value, volumeEnvelope.currentA, volumeEnvelope.currentD, 0.1, volumeEnvelope.currentR)


while True:
    t2 = threading.Thread(target=playNotes, args=()) 
    t2.start()
    GUIupdate()
  
    
