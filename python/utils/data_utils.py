'''
    - Python utils module to work as interface between other modules 
    
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

import numpy as np
import pandas as pd
import os 

import sys
sys.path.insert(1, '/Users/aleir97/Documents/eHand/python/')
import com.arduino as arduino

root_path = r'/Users/aleir97/Documents/eHand/python/models/'

def generate_dataset(files, samples):
    ind =-1
    
    for entry in files:
        print("DATA FROM FILE: "+ entry)

        ind += 1
        signal = pd.read_csv(entry)
        
        ch1, ch2 = signal["CH1"].to_numpy(), signal["CH2"].to_numpy()    
        ch1, ch2  = ch1[1:samples+1], ch2[1:samples+1] 
    
        ch1rms, ch2rms = int (np.round(np.sqrt(np.mean(ch1**2)))), int (np.round(np.sqrt(np.mean(ch2**2))))         
    
        if "rest" in entry:
            mvmnt = 0
        elif 'flex'  in entry:
            mvmnt = 1 
        elif 'ext' in entry:
            mvmnt = 2
        elif 'fist' in entry:
            mvmnt = 3

        data = {'CH1': ch1rms,
        'CH2': ch2rms,
        'class': mvmnt    
        }

        if (ind == 0):
                df = pd.DataFrame(data, columns= ['CH1', 'CH2', 'class'], index = [ind])

        else:
            df2 = pd.DataFrame(data, columns= ['CH1', 'CH2', 'class'], index = [0]) 
            # Deprecated
            # df = df.append(df2, ignore_index= True)
            df  = pd.concat([df2, df], ignore_index=True)

    path = root_path+ 'emg_data.csv' 
    df.to_csv(path, index = False, header=True)    

def get_data(files, used_samples):
    # Function to generate the data
	generate_dataset(files, used_samples)

	path = root_path+ '/emg_data.csv'
	data_csv = pd.read_csv(path)

	data = np.dstack((data_csv["CH1"].to_numpy(dtype= np.float32), data_csv["CH2"].to_numpy(dtype= np.float32)))
	data = data.reshape(data.shape[1:])	

	targets = data_csv['class'].to_numpy(dtype= np.float32)

	return data, targets
