from scipy import signal as sg
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np
from numpy.core.fromnumeric import mean
import pandas as pd
import os 

import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms

freq = 1000 
n = np.arange(1, freq+1)
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
    plt.suptitle(file_name + " FFT:")

    xf = fftfreq(len(n), 1/freq)[:len(n)//2]

    ch1sigf = fft(ch1)
    plt.subplot(211)
    plt.plot(xf, 2.0/len(n) * np.abs(ch1sigf[0:len(n)//2]))
    
    ch1sigf = fft(ch2)
    plt.subplot(212)
    plt.plot(xf, 2.0/len(n) * np.abs(ch1sigf[0:len(n)//2]))
    plt.grid()


def feature_calc(file_name, color, marker, label, feature_name, func, ch):
	treshold_rest, rest_cont, treshold_flex, flex_cont = 0, 0, 0, 0

	
	feature1 = np.sqrt(func(ch[0]))
	feature2 = np.sqrt(func(ch[1]))

	plt.scatter(feature1, feature2, c=color, marker=marker, label=label)
	plt.title('Linearly separable data from '+ feature_name)
	plt.xlabel(feature_name+ ' at CH1')
	plt.ylabel(feature_name+ ' at CH2')

	print(feature_name+ ' FROM CHANNEL 1: '+ str(feature1))
	print(feature_name+ ' FROM CHANNEL 2: '+ str(feature2))

	return feature1, feature2 
 
def analysis(files, options):
	# Signal features in time domain
	treshold_rest_rms, treshold_flex_rms, rest_cont_rms, flex_cont_rms = 0, 0, 0, 0 
	treshold_rest_mean, treshold_flex_mean, rest_cont_mean, flex_cont_mean = 0, 0, 0, 0  
	ext, rest, fist, flex = False, False, False, False

	for entry in files:
		print("DATA FROM FILE: "+ entry)
		signal = pd.read_csv(entry)
		ch1 = signal["CH1"].to_numpy()
		ch2 = signal["CH2"].to_numpy()    

		#order = 5
		#lowcut = 40 / (freq/2)
		#b, a = sg.butter(order, lowcut, 'low', analog=False)
		#ch1 = sg.lfilter(b, a, ch1)
		#ch2 = sg.lfilter(b, a, ch2)
            
		color, marker, label = '','',''	
		if "ext" in entry:
			color = 'yellow'
			marker = 'o'
			label = 'Extension' if ext==False else '_'
			ext = True

		elif 'rest'  in entry:
			color= 'blue' 
			marker = '8'
			label = 'Reposo' if rest==False else '_'
			rest = True

		elif 'fist' in entry:
			color= 'black'
			marker = 'p'
			label = 'Cierre de puño' if fist==False else '_'
			fist = True

		elif 'flex' in entry:
			color = 'coral'
			marker = 's'
			label = 'Flexion' if flex==False else '_'
			flex = True
		
		if options[0]:
			plt.figure(1)
			plt.legend() 
			plt.grid()
			feature1, _ = feature_calc(entry, color, marker, label, "Mean", np.mean, [ch1, ch2])

			if 'rest' in entry:
				treshold_rest_mean += feature1
				rest_cont_mean += 1 
        
			elif 'flex' in entry:
				treshold_flex_mean += feature1
				flex_cont_mean += 1

		if options[1]:
			plt.figure(2)
			plt.legend() 
			plt.grid()

			def rms_calc(x):
				return np.mean(x**2)	
			feature1, _ = feature_calc(entry, color, marker, label, "RMS", rms_calc, [ch1, ch2])

			if 'rest' in entry:
				treshold_rest_rms += feature1
				rest_cont_rms += 1 
        
			elif 'flex' in entry:
				treshold_flex_rms += feature1
				flex_cont_rms += 1
       
		if options[2]:
			plt.figure(3)
			plot_fft(entry, ch1, ch2)
   	 
	if options[0] and (ext+ rest+ fist+ flex == 2):
		treshold_mean = (treshold_flex_mean/flex_cont_mean + treshold_rest_mean/rest_cont_mean) /2
		plt.figure(1) 
		plt.axvline(treshold_mean, color='red')
		print(treshold_mean)

	if options[1] and (ext+ rest+ fist+ flex == 2):
		treshold_rms = (treshold_flex_rms/flex_cont_rms + treshold_rest_rms/rest_cont_rms) /2
		plt.figure(2) 
		plt.axvline(treshold_rms, color='red')
		print(treshold_rms)

	plt.show()

def main():
    dire = r'D:\\PROYECTO_MANO_FPGA\\GIT\\measures\\25-2021-11-Alberto-Umbral'
    #analysis(dire)

if __name__ == "__main__":
    main()
