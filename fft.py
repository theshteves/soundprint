import numpy
import aubio
import math
from aubio import pitch

samplerate = 44100
hop = 2048


def mag(v):
    return numpy.absolute(v)

def find_freq(samples):
    global samplerate
    global hop
    transform = numpy.fft.fft(samples)
    mags = []
    for t in transform:
        mags.append(mag(t))


    sig_freqs = []
    for i in range(0, len(mags)/2):
        if mags[i] > 0.2*hop:
            #print i*samplerate/hop, mags[i]
            sig_freqs.append(i*samplerate/hop)
    
    sum = 0
    c = 0
    for freq in sig_freqs:
        if freq < 4000:
            sum = sum + freq
            c = c + 1

    small_avg = 0
    if c > 0:
        small_avg = sum/c
        small_avg = int(round(round(small_avg/50.0)*50))

    sum = 0
    c = 0
    for freq in sig_freqs:
        if freq > 4000:
            sum = sum + freq
            c = c + 1
    large_avg = 0
    if c > 0:
        large_avg = sum/c
        large_avg = int(round(round(large_avg/50.0)*50))

    
    return small_avg, large_avg


def decode(fname):
    s = aubio.source(fname, samplerate, hop)


    frames = []

    while True:
        samples, reads = s()
        if reads == 0:
            break
        frames.extend(samples[0:reads])

    #print len(frames)
    max_amp = max(frames)
    #print max_amp


    for i in range(0, len(frames)):
        frames[i] = frames[i]/max_amp

    #print max(frames)


    start = 0
    while frames[start] < 0.3:
        start = start+1
    end = len(frames)-1
    while frames[end] < 0.3:
        end = end-1

    samples = frames[start:end]





    #print max(samples)

    x = 0

    #print len(samples)
    freqs = []
    while x + 2048 < len(samples):
        freqs.append(find_freq(samples[x+20:x+20 + 2048]))
#        print "-----------"
        x = x + 2205    
#    print freqs
        
    base64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    bits = ''   

    for x in freqs:
        y = x[0]
        z = x[1]
        b64 = (y-400)/50
        b642 = (z-4500)/50 
        bits = bits + base64[b64] + base64[b642]
#    print len(bits)*6/8
    return bits




print decode('test.wav')
