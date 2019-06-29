import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt



chunk=1024*4
Format=pyaudio.paInt16
Channel=1
Rate=44100

p=pyaudio.PyAudio()
stream=p.open(format=Format,
              channels=Channel,rate=Rate,input=True,output=True,frames_per_buffer=chunk)



fig,ax=plt.subplots()
x=np.arange(0,2*chunk,2)
line,=ax.plot(x,np.random.rand(chunk))
ax.set_ylim(0,255)
ax.set_xlim(0,chunk)

while True:
    data=stream.read(chunk)
    data_int=np.array(struct.unpack(str(2*chunk) + 'B',data),dtype='b')
    line.set_ydata(data_int)
    fig.canvas.draw()
    fig.canvas.flush_events()

fix,ax=plt.subplots()
