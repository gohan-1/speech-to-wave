try :   
    import pyaudio
    import wave
    import numpy as np
    import scipy.io.wavfile
    import math
    import numpy as np
    import pandas as pd
    import scipy.io.wavfile
    import math
    from pandas import ExcelWriter
    import matplotlib.pyplot as plt
    from pandas import ExcelFile
    import warnings
    
    import json
    import os
    import re
    import sys
    from subprocess import Popen, PIPE
    from math import log, ceil
    from tempfile import TemporaryFile
    from warnings import warn
    from functools import wraps
    from pydub import AudioSegment 
    import speech_recognition as sr 
    from pydub.playback import play
except:
    print("something not installed")


warnings.simplefilter('ignore', DeprecationWarning)
i=0
f,ax = plt.subplots(2)

# Prepare the Plotting Environment with random starting values
x = np.arange(10000)
y = np.random.randn(10000)

# Plot 0 is for raw audio data
li, = ax[0].plot(x, y)
ax[0].set_xlim(0,1000)
ax[0].set_ylim(-5000,5000)
ax[0].set_title("Raw Audio Signal")
# Plot 1 is for the FFT of the audio
li2, = ax[1].plot(x, y)
ax[1].set_xlim(0,5000)
ax[1].set_ylim(-100,100)
ax[1].set_title("Fast Fourier Transform")
# Show the plot, but without blocking updates
plt.pause(0.01)
plt.tight_layout()
outputFile = "outputFigure.png"
FORMAT = pyaudio.paInt16 # We use 16bit format per sample
CHANNELS = 2
RATE = 44100
CHUNK = 1024 # 1024bytes of data red from a buffer
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()
frames=[]
global keep_going
keep_going = True
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")
Value=int(RATE / CHUNK * RECORD_SECONDS)
frames = []
def plot_data(in_data):
    # get and convert the data to float
    audio_data = np.fromstring(in_data, np.int16)
    
    # Fast Fourier Transform, 10*log10(abs) is to scale it to dB
    # and make sure it's not imaginary
    dfft = 10.*np.log10(abs(np.fft.rfft(audio_data)))

    # Force the new data into the plot, but without redrawing axes.
    # If uses plt.draw(), axes are re-drawn every time
    #print audio_data[0:10]
    #print dfft[0:10]
    #print
    li.set_xdata(np.arange(len(audio_data)))
    li.set_ydata(audio_data)
    li2.set_xdata(np.arange(len(dfft))*10.)
    li2.set_ydata(dfft)

    # Show the updated plot, but without blocking
    plt.pause(0.02)
    
try:
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
   
        Streaming=stream.read(CHUNK)
        plot_data(Streaming)
        frames.append(Streaming)
    plt.close(f)
    
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    

    rate, data = scipy.io.wavfile.read('output.wav')
    
    data2 = []
    


    for i in range(len(data)):
        
        data2.append([int(round(math.sin(data[i][0])*3000)), int(round(math.sin(data[i][1])*3000))])
       

    data2 = np.asarray(data2)

    
    
    #plotting
    spf = wave.open(WAVE_OUTPUT_FILENAME,'r')
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')

    fig = plt.figure(1)
    plt.title('Signal Wave...')
    plt.plot(signal)
    

    fig.savefig(outputFile)


    rate, data = scipy.io.wavfile.read('output.wav')

    data2 = []
    
    for i in range(len(data)):
        data2.append([int(round(math.sin(data[i][0])*3000)), int(round(math.sin(data[i][1])*3000))])

    data2 = np.asarray(data2)


    
    df=pd.DataFrame(data2)
    df.columns=["x","y"]
    writer = ExcelWriter('wave.xlsx')
    df.to_excel(writer,'Sheet1',index=False)
    
    writer.save()
except:
    print("something went ")

    
  
# Input audio file to be sliced 
audio = AudioSegment.from_wav("output.wav") 
audio_segment=audio



def db_to_float(db, using_amplitude=True):
    """
    Converts the input db to a float, which represents the equivalent
    ratio in power.
    """
    db = float(db)
    if using_amplitude:
        return 10 ** (db / 20)
    else:  # using power
        return 10 ** (db / 10)


import itertools




def detect_silence(audio_segment, min_silence_len=1000, silence_thresh=-22, seek_step=1):
    seg_len = len(audio_segment)

    # you can't have a silent portion of a sound that is longer than the sound
    if seg_len < min_silence_len:
        return []

    # convert silence threshold to a float value (so we can compare it to rms)
    silence_thresh = db_to_float(silence_thresh) * audio_segment.max_possible_amplitude
    

    # find silence and add start and end indicies to the to_cut list
    silence_starts = []

    # check successive (1 sec by default) chunk of sound for silence
    # try a chunk at every "seek step" (or every chunk for a seek step == 1)
    last_slice_start = seg_len - min_silence_len
    slice_starts = range(0, last_slice_start + 1, seek_step)

    # guarantee last_slice_start is included in the range
    # to make sure the last portion of the audio is seached
    if last_slice_start % seek_step:
        slice_starts = itertools.chain(slice_starts, [last_slice_start])

    for i in slice_starts:
        audio_slice = audio_segment[i:i + min_silence_len]
        
        if audio_slice.rms <= silence_thresh:
            silence_starts.append(i)
    

    # short circuit when there is no silence
    if not silence_starts:
        return []

    # combine the silence we detected into ranges (start ms - end ms)
    silent_ranges = []

    prev_i = silence_starts.pop(0)
    current_range_start = prev_i

    for silence_start_i in silence_starts:
        continuous = (silence_start_i == prev_i + seek_step)

        # sometimes two small blips are enough for one particular slice to be
        # non-silent, despite the silence all running together. Just combine
        # the two overlapping silent ranges.
        silence_has_gap = silence_start_i > (prev_i + min_silence_len)

        if not continuous and silence_has_gap:
            silent_ranges.append([current_range_start,
                                  prev_i + min_silence_len])
            current_range_start = silence_start_i
        prev_i = silence_start_i

    silent_ranges.append([current_range_start,
                          prev_i + min_silence_len])
    
    return silent_ranges


def detect_nonsilent(audio_segment, min_silence_len=1000, silence_thresh=-22, seek_step=1):
    silent_ranges = detect_silence(audio_segment, min_silence_len, silence_thresh, seek_step)
    len_seg = len(audio_segment)

    # if there is no silence, the whole thing is nonsilent
    if not silent_ranges:
        return [[0, len_seg]]

    # short circuit when the whole audio segment is silent
    if silent_ranges[0][0] == 0 and silent_ranges[0][1] == len_seg:
        return []

    prev_end_i = 0
    nonsilent_ranges = []
    for start_i, end_i in silent_ranges:
        nonsilent_ranges.append([prev_end_i, start_i])
        prev_end_i = end_i

    if end_i != len_seg:
        nonsilent_ranges.append([prev_end_i, len_seg])

    if nonsilent_ranges[0] == [0, 0]:
        nonsilent_ranges.pop(0)
    print("Number of Words",len(nonsilent_ranges))
    return nonsilent_ranges


def split_on_silence(audio_segment, min_silence_len=1000, silence_thresh=-22, keep_silence=100,
                     seek_step=1):
    """
    audio_segment - original pydub.AudioSegment() object
    min_silence_len - (in ms) minimum length of a silence to be used for
        a split. default: 1000ms
    silence_thresh - (in dBFS) anything quieter than this will be
        considered silence. default: -16dBFS
    keep_silence - (in ms) amount of silence to leave at the beginning
        and end of the chunks. Keeps the sound from sounding like it is
        abruptly cut off. (default: 100ms)
    """

    not_silence_ranges = detect_nonsilent(audio_segment, min_silence_len, silence_thresh, seek_step)

    chunks = []
    for start_i, end_i in not_silence_ranges:
        start_i = max(0, start_i - keep_silence)
        end_i += keep_silence

        chunks.append(audio_segment[start_i:end_i])
    
    return chunks


def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms
    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms
    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms
Chunks=split_on_silence(audio_segment)
for voice in Chunks:
    play(voice)


