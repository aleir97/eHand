from scipy import signal as sg
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np
from numpy.core.fromnumeric import mean
import pandas as pd

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = sg.butter(order, [low, high], btype='band')
    return b, a


freq = 1000 
n = np.arange(1, 1001)

# Signal features in time domain
for file in ['resting.csv', 'resting2.csv', 'resting3.csv', 'flexion.csv', 'flexion2.csv',  'flexion3.csv', 'extension.csv','extension2.csv','extension3.csv']:
    print("DATA FROM FILE: "+ file)
    signal = pd.read_csv(file)
    ch1 = signal["CH1"].to_numpy()
    ch2 = signal["CH2"].to_numpy()    
    
    order = 5
    lowcut = 40 / (freq/2)
    b, a = sg.butter(order, lowcut, 'low', analog=False)
    ch1 = sg.lfilter(b, a, ch1)
    ch2 = sg.lfilter(b, a, ch2)

    ch1mean = mean(ch1) 
    ch2mean = mean(ch2)
    #print("MEAN OF THE CHANNEL 1: "+ str(ch1mean))
    #print("MEAN OF THE CHANNEL 1: "+ str(ch2mean))
    plt.figure(1)
    plt.scatter(ch1mean, ch2mean)
    plt.title('Linearly separable data from MEAN')
    plt.xlabel('ch1')
    plt.ylabel('ch2')

    ch1rms = np.sqrt(np.mean(ch1**2))
    ch2rms = np.sqrt(np.mean(ch2**2))
    print("RMS FROM CHANNEL 1: "+ str(ch1rms))
    print("RMS FROM CHANNEL 2: "+ str(ch2rms))
    plt.figure(2)
    plt.scatter(ch1rms, ch2rms)
    plt.title('Linearly separable data from RMS')
    plt.xlabel('ch1')
    plt.ylabel('ch2')

    ch1var = np.var(ch1)
    ch2var = np.var(ch2)
    #print("VARIANCE FROM CH1: "+ str(ch1var))
    #print("VARIANCE FROM CH2: "+ str(ch2var))
    plt.figure(3)
    plt.scatter(ch1var, ch2var)
    plt.title('Linearly separable data from VARIANCE')
    plt.xlabel('ch1')
    plt.ylabel('ch2')

plt.show()

# Filter Design
# If you wanna calculate the precise order for filtering
#band_low_pass = 150 / (freq/2) # from Hz to Rad/s
#band_low_stop = 160 / (freq/2)
#band_high_pass = 20 / (freq/2)
#band_high_stop = 10 / (freq/2)
# N, Wn = sg.buttord([band_high_pass, band_low_pass], [band_high_stop, band_low_stop], 3, 60, False)

# Easy way, cuts in Hz
#order= 4
#lowcut= 40 
#highcut= 50
#b, a = butter_bandpass(lowcut, highcut, freq, order)
#w, h = sg.freqz(b, a, worN=2000)

##Plot filter response
#plt.figure(1)
#plt.clf()
#plt.plot((freq * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)
#plt.plot([0, 0.5 * freq], [np.sqrt(0.5), np.sqrt(0.5)], '--', label='sqrt(0.5)')
#plt.xlabel('Frequency (Hz)')
#plt.ylabel('Gain')
#plt.grid(True)
#plt.legend(loc='best')
#
#filt_ch1 = sg.lfilter(b, a, ch1)
#filt_ch2 = sg.lfilter(b, a, ch2)
#
#plt.figure(2)
#plt.subplot(221)
#plt.stem(n, ch1)
#
#plt.subplot(222)
#plt.stem(n, ch2)
#
#plt.subplot(223)
#plt.stem(n, np.abs(filt_ch1))
#
#plt.subplot(224)
#plt.stem(n, np.abs(filt_ch2))
#
#plt.show()

## FFT Analysis
#plt.figure(3)
#
#xf = fftfreq(len(n), 1/freq)[:len(n)//2]
#
#extsigf = fft(extsig)
#plt.subplot(221)
#plt.plot(xf, 2.0/len(n) * np.abs(extsigf[0:len(n)//2]))
#
#restsigf = fft(restsig)
#plt.subplot(222)
#plt.plot(xf, 2.0/len(n) * np.abs(restsigf[0:len(n)//2]))
#
#filt_extf = fft(filt_ext)
#plt.subplot(223)
#plt.plot(xf, 2.0/len(n) * np.abs(filt_extf[0:len(n)//2]))
#
#filt_restf = fft(filt_rest)
#plt.subplot(224)
#plt.plot(xf, 2.0/len(n) * np.abs(filt_restf[0:len(n)//2]))
#
#plt.show()
