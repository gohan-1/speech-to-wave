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