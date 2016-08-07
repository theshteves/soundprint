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
def sinepack(r,a,b=None,c=None,d=None):    
    f1 = ((400 + 30*a)*2*pi) / bitrate
    
    if (b!=None):
        f2 = ((2500 + 30*b)*2*pi) / bitrate
    else:
        f2 = 0
        
    if (c!=None):
        f3 = ((4500 + 30*c)*2*pi) / bitrate
    else:
        f3 = 0
        
    if (d!=None):
        f4 = ((6500 + 30*d)*2*pi) / bitrate
    else:
        f4 = 0
    
    quadrant = maxVol/(4-r)
    
    samples = ""    
    for x in range(frames):        
        samples += pack ('h', ((quadrant*sin(x*f1))+(quadrant*sin(x*f2))+(quadrant*sin(x*f3))+(quadrant*sin(x*f4))))
    return samples

elements = {x:n for n,x in enumerate(base_64)}

#encode text here
usertext = "Base64 is a generic term for a number of similar encoding schemes that encode binary data by treating it numerically and translating it into a base 64 representation. The Base64 term originates from a specific MIME content transfer encoding."
encoded = base64.urlsafe_b64encode(usertext) #replaces + with - and / with _

#create sound file by starting stream
wf = wave.open('soundprint4.wav', 'w')
wf.setparams((1,2,bitrate,0,'NONE','not compressed'))

#convert each char in 64base string into sound
enc_loop = encoded.replace('=', '')
r = len(enc_loop)%4
for c in range(0, len(enc_loop)-r, 4):
    a, b, e, f = enc_loop[c], enc_loop[c+1],enc_loop[c+2],enc_loop[c+3]     
    wf.writeframes(sinepack(0,elements[a],elements[b],elements[e],elements[f]))
    
for c in range(len(enc_loop)-r,len(enc_loop),r):
    if (r==1):
        a = enc_loop[c]
        wf.writeframes(sinepack(r,elements[a]))
    elif (r==2):
        a,b = enc_loop[c], enc_loop[c+1]
        wf.writeframes(sinepack(r,elements[a],elements[b]))
    elif (r==3):
        a,b,c = enc_loop[c], enc_loop(c+1), enc_loop(c+2)
        wf.writeframes(sinepack(r,elements[a],elements[b],elements[e]))    
wf.close

