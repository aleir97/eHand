from scipy import signal as sg
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np
from numpy.core.fromnumeric import mean


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = sg.butter(order, [low, high], btype='band')
    return b, a


freq = 1000 
n = np.arange(1, 1000)

extsig = np.genfromtxt('D:\PROYECTO_MANO_FPGA\GIT\PY\ANALYSIS\extension.txt', delimiter='\n').astype(int)
extsig = extsig[1:len(n)+1]

restsig =np.genfromtxt('D:\PROYECTO_MANO_FPGA\GIT\PY\ANALYSIS\\resting.txt', delimiter='\n').astype(int)
restsig = restsig[1:len(n)+1]


# Signal features in time domain
meanext = mean(extsig) 
print(meanext)
meanrest = mean(restsig)
print(meanrest)

# Filter Design
# If you wanna calculate the precise order for filtering
#band_low_pass = 150 / (freq/2) # from Hz to Rad/s
#band_low_stop = 160 / (freq/2)
#band_high_pass = 20 / (freq/2)
#band_high_stop = 10 / (freq/2)
# N, Wn = sg.buttord([band_high_pass, band_low_pass], [band_high_stop, band_low_stop], 3, 60, False)

# Easy way, cuts in Hz
order = 5
lowcut = 20
highcut= 100
b, a = butter_bandpass(lowcut, highcut, freq, order)
w, h = sg.freqz(b, a, worN=2000)

# Plot filter response
plt.figure(1)
plt.clf()
plt.plot((freq * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)
plt.plot([0, 0.5 * freq], [np.sqrt(0.5), np.sqrt(0.5)], '--', label='sqrt(0.5)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain')
plt.grid(True)
plt.legend(loc='best')

filt_ext = sg.lfilter(b, a, extsig)
filt_rest = sg.lfilter(b, a, restsig)

plt.figure(2)
plt.subplot(221)
plt.stem(n, extsig)

plt.subplot(222)
plt.stem(n, restsig)

plt.subplot(223)
plt.stem(n, np.abs(filt_ext))

plt.subplot(224)
plt.stem(n, np.abs(filt_rest))

# FFT Analysis
plt.figure(3)

xf = fftfreq(len(n), 1/freq)[:len(n)//2]

extsigf = fft(extsig)
plt.subplot(221)
plt.plot(xf, 2.0/len(n) * np.abs(extsigf[0:len(n)//2]))

restsigf = fft(restsig)
plt.subplot(222)
plt.plot(xf, 2.0/len(n) * np.abs(restsigf[0:len(n)//2]))

filt_extf = fft(filt_ext)
plt.subplot(223)
plt.plot(xf, 2.0/len(n) * np.abs(filt_extf[0:len(n)//2]))

filt_restf = fft(filt_rest)
plt.subplot(224)
plt.plot(xf, 2.0/len(n) * np.abs(filt_restf[0:len(n)//2]))

plt.show()
