'''
    - Python module to synchronize between serial device and PC to acquire and measure EMG samples
    
	Copyright (C) 2021 Alejandro Iregui Valcarcel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import winsound
import pandas as pd
import matplotlib.pyplot as plt 
import os
from datetime import datetime
import com.arduino as arduino


date = datetime.today().strftime('%d-%Y-%m')
measure_dir =  r"..\emg_data"+ '\\'+ date

if (os.path.isdir(measure_dir) == False):
    os.mkdir(measure_dir)

def save_csv(A1, A2, file):
    data = {'CH1': A1,
            'CH2': A2}

    df = pd.DataFrame(data, columns= ['CH1', 'CH2'])
    
    path = measure_dir+ '\\'+ file+ '.csv' 
    df.to_csv (path, index = False, header=True)

def make_sound():
    #Sound parameters
    frequency = 500  # Set Frequency To 500 Hertz
    duration = 2000  # Set Duration To 2000 ms == 2 second
    winsound.Beep(frequency, duration)

def plot_measures(samp):
	title = "CH{channel:d}:"

	plt.figure()
	ax = plt.subplot(samp.shape[0]*100+11)

	for i in range(samp.shape[0]):
		ax = plt.subplot(210+i+1)
		ax.set_title(title.format(channel=i+1))
		plt.plot(samp[i])

	plt.show()

def make_measures(name_fl, port, n_channels, n_samples):
	make_sound()

	samples = arduino.read_samples(port, n_samples, n_channels)
	plot_measures(samples)

	file = name_fl 
	# TODO: Multiple channel .csv save
	save_csv(samples[0], samples[1], file)