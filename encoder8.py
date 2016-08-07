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
def sinepack(r,a,b=None,c=None,d=None,e=None,f=None,g=None,h=None):    
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
        
    if (e!=None):
        f5 = ((8500 + 30*e)*2*pi) / bitrate
    else:
        f5 = 0
        
    if (f!=None):
        f6 = ((10500 + 30*f)*2*pi) / bitrate
    else:
        f6 = 0
        
    if (g!=None):
        f7 = ((12500 + 30*g)*2*pi) / bitrate
    else:
        f7 = 0
        
    if (h!=None):
        f8 = ((14500 + 30*h)*2*pi) / bitrate
    else:
        f8 = 0
    
    quadrant = maxVol/(8-r)
    
    samples = ""    
    for x in range(frames):        
        samples += pack ('h', ((quadrant*sin(x*f1))+(quadrant*sin(x*f2))+(quadrant*sin(x*f3))+(quadrant*sin(x*f4)+(quadrant*sin(x*f5))+(quadrant*sin(x*f6))+(quadrant*sin(x*f7))+(quadrant*sin(x*f8)))))

    return samples

elements = {x:n for n,x in enumerate(base_64)}

#encode text here
usertext = "Base64 is a generic term for a number of similar encoding schemes that encode binary data by treating it numerically and translating it into a base 64 representation. The Base64 term originates from a specific MIME content transfer encoding."
encoded = base64.urlsafe_b64encode(usertext) #replaces + with - and / with _

#create sound file by starting stream
wf = wave.open('soundprint8.wav', 'w')
wf.setparams((1,2,bitrate,0,'NONE','not compressed'))

#convert each char in 64base string into sound
enc_loop = encoded.replace('=', '')
r = len(enc_loop)%8
for c in range(0, len(enc_loop)-r, 8):
    a, b, d, e, f, g, h, i = enc_loop[c], enc_loop[c+1],enc_loop[c+2],enc_loop[c+3],enc_loop[c+4], enc_loop[c+5],enc_loop[c+6],enc_loop[c+7]     
    wf.writeframes(sinepack(0,elements[a],elements[b],elements[d],elements[e],elements[f],elements[g],elements[h],elements[i]))
    
for c in range(len(enc_loop)-r,len(enc_loop),r):
    if (r==1):
        a = enc_loop[c]
        wf.writeframes(sinepack(r,elements[a]))
    elif (r==2):
        a,b = enc_loop[c], enc_loop[c+1]
        wf.writeframes(sinepack(r,elements[a],elements[b]))
    elif (r==3):
        a,b,c = enc_loop[c], enc_loop(c+1), enc_loop(c+2)
        wf.writeframes(sinepack(r,elements[a],elements[b],elements[c]))
    elif (r==4):
        a,b,c,d = enc_loop[c], enc_loop(c+1), enc_loop(c+2), enc_loop(c+3)
        wf.writeframes(sinepack(r,elements[a],elements[b],elements[c], elements[d]))    
    elif (r==5):
        a,b,c,d,e = enc_loop[c], enc_loop(c+1), enc_loop(c+2), enc_loop(c+3), enc_loop(c+4)
        wf.writeframes(sinepack(r,elements[a],elements[b],elements[c],elements[d],elements[e]))    
    elif (r==6):
        a,b,c,d,e,f = enc_loop[c], enc_loop(c+1), enc_loop(c+2), enc_loop(c+3), enc_loop(c+4), enc_loop(c+5)
        wf.writeframes(sinepack(r,elements[a],elements[b],elements[c],elements[d],elements[e],elements[f]))    
    elif (r==7):
        a,b,c,d,e,f,g = enc_loop[c], enc_loop(c+1), enc_loop(c+2), enc_loop(c+3), enc_loop(c+4), enc_loop(c+5), enc_loop(c+6)
        wf.writeframes(sinepack(r,elements[a],elements[b],elements[c],elements[d],elements[e],elements[f],elements[c],elements[d],elements[e],elements[g]))    
wf.close

