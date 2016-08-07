#import pyaudio
#import numpy as np
from __future__ import division
import sys
import math
import wave
import struct
import argparse
from itertools import *
import base64

#initiate pyaudio
#p = pyaudio.PyAudio()
#set parameters
#volume = 1.0     # range [0.0, 1.0]
bitrate = 44100       # sampling rate, Hz, must be integer
duration = 0.01   # in seconds, may be float
#f = 440.0        # sine frequency, Hz, may be float

#create 2d list with each base-64 char linking to the respective sine wave frequency 
base_64 = [chr(x) for x in (range(65,91)+range(97,123)+range(48,58)+[45,95])]

def mysine(i):
    frequency = 400 + 50*i
    frames = int(bitrate*duration)
    samples = ''
    '''global amplitude
    
    period = int(bitrate / frequency)
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0
    lookup_table = [float(amplitude) * math.sin(2.0*math.pi*float(frequency)*(float(i%period)/float(bitrate))) for i in xrange(period)]
    return (lookup_table[i%period] for i in count(bitrate*amplitude))'''
    for x in range(frames):        
        samples = samples+chr(int(math.sin(x/((bitrate/frequency)/(2*math.pi)))*127+128))
    #(np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32) #generates sine wave using numpy
    return samples    
   
    
elements = {x: mysine(n) for n, x in enumerate(base_64)}

'''
import pprint
p = pprint.PrettyPrinter(width=50)
p.pprint(elements)
'''

#encode text
usertext = 'Base64 is a generic term for a number of similar encoding schemes that encode binary data by treating it numerically and translating it into a base 64 representation. The Base64 term originates from a specific MIME content transfer encoding.'
encoded = base64.urlsafe_b64encode(usertext) #replaces + with - and / with _
#encoded
#create sound file by starting stream
wf = wave.open('soundprint.wav', 'w')
wf.setparams((1,1,bitrate,0,'NONE','not compressed'))
#convert each char in 64base string into sound
for c in encoded.replace('=', ''):
    wf.writeframes(elements[c])
    #wf.writeframes(''.join([x for x in elements[c]]))
wf.close

'''
#for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                input=True)
'''
'''   
#stream.write(data)


#stream.stop_stream()
#stream.close()

#p.terminate()

'''

