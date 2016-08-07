from __future__ import division
import sys
from math import sin,pi
import wave
import base64
from struct import pack

#set parameters
bitrate = 44100       # sampling rate, Hz, must be integer
duration = 0.05   # in seconds, may be float
frames = int(bitrate*duration) #total framerate
maxVol=2**15-1.0  #max vol in decibels

#create 2d list with each base-64 char linking to the respective sine wave frequency 
base_64 = [chr(x) for x in (range(65,91)+range(97,123)+range(48,58)+[45,95])]

#Create mono sine wave superimposed from 2 waves
def sinepack(a,b):    
    frequency1 = 400 + 50*a
    frequency2 = 4500 + 50*b
    samples = ""    
    for x in range(frames):        
        samples += pack ('h', (maxVol*sin(x*frequency1*2*pi/bitrate)/2)+(maxVol*sin(x*frequency2*2*pi/bitrate)/2))        
    return samples
 
elements = {x:n for n,x in enumerate(base_64)}

#encode text here
usertext = "Insert text here"
encoded = base64.urlsafe_b64encode(usertext) #replaces + with - and / with _

#create sound file by starting stream
wf = wave.open('soundprint.wav', 'w')
wf.setparams((1,2,bitrate,0,'NONE','not compressed'))

#convert each char in 64base string into sound
enc_loop = encoded.replace('=', '')
for c in range(0, len(enc_loop), 2):
    a, b = enc_loop[c], enc_loop[c+1]   
    wf.writeframes(sinepack(elements[a],elements[b]))    
wf.close

