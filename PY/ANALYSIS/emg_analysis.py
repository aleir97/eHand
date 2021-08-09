from scipy import signal as sg
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np
from numpy.core.fromnumeric import mean
import pandas as pd
import os 

def butter_bandpass(fs, lowcut, highcut=None, order=None):
    if (highcut == None & order == None):
        fstop = lowcut / (0.5 * fs)
        fpass = fs - 20
         
        N, Wn = sg.buttord([fpass, fstop], 5, 60, False)
        b, a = sg.butter(N, lowcut, 'low', analog=False)    

        return b,a
    
    elif(highcut == None):
        lowcut = lowcut / (0.5 * fs)
        b, a = sg.butter(order, lowcut, 'low', analog=False)    

        return b,a    

    # Filter Design
    # If you wanna calculate the precise order for filtering
    #band_low_pass = 150 / (freq/2) # from Hz to Rad/s
    #band_low_stop = 160 / (freq/2)
    #band_high_pass = 20 / (freq/2)
    #band_high_stop = 10 / (freq/2)
    #N, Wn = sg.buttord([band_high_pass, band_low_pass], [band_high_stop, band_low_stop], 3, 60, False)

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
        
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = sg.butter(order, [low, high], btype='band')
    return b, a

def plot_fft(file_name, ch1, ch2):
    plt.figure()
    plt.suptitle(file_name + " FFT:")

    xf = fftfreq(len(n), 1/freq)[:len(n)//2]

    ch1sigf = fft(ch1)
    plt.subplot(211)
    plt.plot(xf, 2.0/len(n) * np.abs(ch1sigf[0:len(n)//2]))
    
    ch1sigf = fft(ch2)
    plt.subplot(212)
    plt.plot(xf, 2.0/len(n) * np.abs(ch1sigf[0:len(n)//2]))


freq = 1000 
n = np.arange(1, 1001)
 
def main():
    # Signal features in time domain
    dire = r'D:\PROYECTO_MANO_FPGA\GIT\PY\ANALYSIS\data_analysis'

    for entry in os.scandir(dire):
        if (entry.is_file()):
            print("DATA FROM FILE: "+ entry.name)
            signal = pd.read_csv(entry.path)
            ch1 = signal["CH1"].to_numpy()
            ch2 = signal["CH2"].to_numpy()    

            #order = 5
            #lowcut = 40 / (freq/2)
            #b, a = sg.butter(order, lowcut, 'low', analog=False)
            #ch1 = sg.lfilter(b, a, ch1)
            #ch2 = sg.lfilter(b, a, ch2)
            
            color = ''
            if "ext" in entry.name:
                color = 'red'
            elif 'rest'  in entry.name:
                color= 'blue' 
            elif 'fist' in entry.name:
                color= 'black'
            elif 'flex' in entry.name:
                color = 'coral'

            #plt.figure(1)
            #ax = plt.subplot(211)
            #ax.set_title(entry.name + ", CH1:")
            #plt.stem(n, ch1)

            #ax = plt.subplot(212)
            #ax.set_title("CH2:")
            #plt.stem(n, ch2)

            #feature_name = 'Mean'
            #feature1 = np.sqrt(np.mean(ch1))
            #feature2 = np.sqrt(np.mean(ch2))
            #print("Mean FROM CHANNEL 1: "+ str(feature1))
            #print("Mean FROM CHANNEL 2: "+ str(feature2))

            #feature_name = 'RMS'
            #feature1 = np.sqrt(np.mean(ch1**2))
            #feature2 = np.sqrt(np.mean(ch2**2))
            #print("RMS FROM CHANNEL 1: "+ str(feature1))
            #print("RMS FROM CHANNEL 2: "+ str(feature2))

            plt.figure(2)
            plt.scatter(feature1, feature2, c=color)
            plt.title('Linearly separable data from '+ feature_name)
            plt.xlabel('ch1')
            plt.ylabel('ch2')

            #plot_fft(entry.name, ch1, ch2)
    plt.show()

if __name__ == "__main__":
    main()