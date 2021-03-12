#!/bin/python
import sys
from subprocess import call, Popen, PIPE

def write_to_file(var, path):
    x = open(path, 'w')
    x.write(var)
    x.close()

txt = 'out.txt'
while True:
    p = Popen(['tail', '-1',txt],shell=False, stdout=PIPE)
    ooutput = str(p.stdout.read())
    boutput = ooutput.replace(r'\n','').replace('b','').replace("'","")
    try:
        output = int(boutput.split()[1][:boutput.index('.')])
    except:
        continue
    print(output)
    if output < 440:
        write_to_file('0','/sys/class/leds/input17::numlock/brightness')
        write_to_file('0', '/sys/class/leds/input17::capslock/brightness')
        write_to_file('1', '/sys/class/leds/input17::scrolllock/brightness')
    elif output < 1000:
        write_to_file('0','/sys/class/leds/input17::numlock/brightness')
        write_to_file('1', '/sys/class/leds/input17::capslock/brightness')
        write_to_file('1', '/sys/class/leds/input17::scrolllock/brightness')
    else:
        write_to_file('1','/sys/class/leds/input17::numlock/brightness')
        write_to_file('1', '/sys/class/leds/input17::capslock/brightness')
        write_to_file('1', '/sys/class/leds/input17::scrolllock/brightness')



