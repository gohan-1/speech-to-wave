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


CHUNK = 1024
outputFile = "outputFigure.png"
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

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
plt.show(block=False)


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