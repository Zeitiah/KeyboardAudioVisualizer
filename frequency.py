#!/bin/python
import aubio
import subprocess 
import pyaudio
from time import sleep

def write_to_input(path, switch):
    x = open(path,'w')
    x.write(switch)
    x.close()
def get_pitches(path):
    src = aubio.source(path)
    hop_size = src.hop_size
    pyaudio_object = pyaudio.PyAudio()
    stream = pyaudio_object.open(format=pyaudio.paFloat32, channels=src.channels, rate=src.samplerate, output=True)
    pitch_object = aubio.pitch(samplerate=src.samplerate)

    while True:
        samples, read = src()
        byte_samples = bytes()
        for i in samples:
            byte_samples += bytes(i)
        stream.write(byte_samples)
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

        if read < src.hop_size:
            break
    stream.stop_stream()
    stream.close()
    pyaudio_object.terminate()
    print('Finished get_pitches')
    return pitches

if __name__ == '__main__':
    # Length is 24291
    for i in get_pitches('036-XenobladeChroniclesOST-GaurPlain.mp3'):
        if i < 25:
            write_to_input('/sys/class/leds/input17::scrolllock/brightness', '0') 
            write_to_input('/sys/class/leds/input17::capslock/brightness', '0') 
            write_to_input('/sys/class/leds/input17::numlock/brightness', '0') 
        elif i < 440:
            write_to_input('/sys/class/leds/input17::scrolllock/brightness', '1') 
            write_to_input('/sys/class/leds/input17::capslock/brightness', '0') 
            write_to_input('/sys/class/leds/input17::numlock/brightness', '0') 
        elif i < 1100:
            write_to_input('/sys/class/leds/input17::scrolllock/brightness', '1') 
            write_to_input('/sys/class/leds/input17::capslock/brightness', '1') 
            write_to_input('/sys/class/leds/input17::numlock/brightness', '0') 
        else:
            write_to_input('/sys/class/leds/input17::scrolllock/brightness', '1') 
            write_to_input('/sys/class/leds/input17::capslock/brightness', '1') 
            write_to_input('/sys/class/leds/input17::numlock/brightness', '1') 
        sleep(0.01)

