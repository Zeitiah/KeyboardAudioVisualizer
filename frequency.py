#!/bin/python
import aubio
import subprocess 
import pyaudio
from time import sleep

def write_to_input(path, switch):
    x = open(path,'w')
    x.write(switch)
    x.close()
def array_to_byte(numpy_array):
    # pyaudio cannot play sound from numpy arrays
    # The contents must all me converted into one byte object
    byte_samples = bytes()
    for i in numpy_array:
        byte_samples += bytes(i)
    return byte_samples
def main(path):
    src = aubio.source(path)
    hop_size = src.hop_size
    pitch_object = aubio.pitch(samplerate=src.samplerate)
    pyaudio_object = pyaudio.PyAudio()
    stream = pyaudio_object.open(format=pyaudio.paFloat32, channels=src.channels, rate=src.samplerate, output=True)

    while True:
        samples, read = src()
        stream.write(array_to_byte(samples))
        pitch = pitch_object(samples)
        if pitch[0] < 25:
            write_to_input('/sys/class/leds/input17::scrolllock/brightness', '0') 
            write_to_input('/sys/class/leds/input17::capslock/brightness', '0') 
            write_to_input('/sys/class/leds/input17::numlock/brightness', '0') 
        elif pitch[0] < 440:
            write_to_input('/sys/class/leds/input17::scrolllock/brightness', '1') 
            write_to_input('/sys/class/leds/input17::capslock/brightness', '0') 
            write_to_input('/sys/class/leds/input17::numlock/brightness', '0') 
        elif pitch[0] < 1100:
            write_to_input('/sys/class/leds/input17::scrolllock/brightness', '1') 
            write_to_input('/sys/class/leds/input17::capslock/brightness', '1') 
            write_to_input('/sys/class/leds/input17::numlock/brightness', '0') 
        else:
            write_to_input('/sys/class/leds/input17::scrolllock/brightness', '1') 
            write_to_input('/sys/class/leds/input17::capslock/brightness', '1') 
            write_to_input('/sys/class/leds/input17::numlock/brightness', '1') 

        if read < hop_size:
            break
    stream.stop_stream()
    stream.close()
    pyaudio_object.terminate()
    return True

if __name__ == '__main__':
    main('036-XenobladeChroniclesOST-GaurPlain.mp3')
    
