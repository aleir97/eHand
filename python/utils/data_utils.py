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

def generate_dataset(samples):
    read_path = root_path+ '/dataset'
    ind =-1
    
    for entry in os.scandir(read_path):
        print(entry)
        if (entry.is_file()):
            ind += 1
            
            signal = pd.read_csv(entry.path)
            
            ch1, ch2 = signal["CH1"].to_numpy(), signal["CH2"].to_numpy()    
            ch1, ch2  = ch1[1:samples+1], ch2[1:samples+1] 
        
            ch1rms, ch2rms = int (np.round(np.sqrt(np.mean(ch1**2)))), int (np.round(np.sqrt(np.mean(ch2**2))))         
        
            if "rest" in entry.name:
                mvmnt = 0
            elif 'flex'  in entry.name:
                mvmnt = 1 
            elif 'ext' in entry.name:
                mvmnt = 2
            elif 'fist' in entry.name:
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

def get_data(used_samples):
    # Function to generate the data
	generate_dataset(used_samples)

	path = root_path+ '/emg_data.csv'
	data_csv = pd.read_csv(path)

	data = np.dstack((data_csv["CH1"].to_numpy(dtype= np.float32), data_csv["CH2"].to_numpy(dtype= np.float32)))
	data = data.reshape(data.shape[1:])	

	targets = data_csv['class'].to_numpy(dtype= np.float32)

	return data, targets

# TODO: Make a Control class for the different classification methods, such as treshold, svm or nnet
from enum import IntEnum, auto
class pose_states(IntEnum):
    EXT   = 0
    FLEX  = auto()
    NEY   = auto()
    PEACE = auto()
    ROCK  = auto()
    SEÑ   = auto()
    END = auto()

def get_state(pose, com_fl, order):
    if pose.value == pose_states.EXT:
        com_fl.seek(0)
        com_fl.write('EXT\n')
        com_fl.truncate()
        return (pose+order) % pose_states.END

    if pose == pose_states.FLEX:
        com_fl.seek(0)
        com_fl.write('FLEX\n')
        com_fl.truncate()
        return (pose+order) % pose_states.END

    if pose == pose_states.NEY:
        com_fl.seek(0)
        com_fl.write('NEY\n')
        com_fl.truncate()
        return (pose+order) % pose_states.END

    if pose == pose_states.PEACE:
        com_fl.seek(0)
        com_fl.write('PEACE\n')
        com_fl.truncate()
        return (pose+order) % pose_states.END

    if pose == pose_states.ROCK:
        com_fl.seek(0)
        com_fl.write('ROCK\n')
        com_fl.truncate()
        return (pose+order) % pose_states.END


def classification_state_machine(used_samples, model):
    # TODO: Conexion con el arduino, lectura de used samples 
    # hacer una "libreria que me devuelva resultados" y otra para inyectarselos algo concurrente (?)
    
    f = open("D:\\PROYECTO_MANO_FPGA\\GIT\\python\\3D\\com.txt", "w")
    state = ''

    online, port = arduino.serial_connection()
    n_samples = 256
    hits = 0
    last_predict = 0
    input('THE MODEL IS READY TO CLASSIFY, PLS PRESS ENTER TO CONNECT TO THE ARDUINO AND BEGIN')

    while True:
        samples = arduino.read_samples(port, n_samples, 2)

        ch1rms, ch2rms = int (np.round(np.sqrt(np.mean(samples[0]**2)))), int (np.round(np.sqrt(np.mean(samples[0]**2))))    
        
        hand_mvn = model.predict([ch1rms, ch2rms])[0]
        print(hand_mvn)

        if last_predict == hand_mvn:
            hits += 1
        else:
            hits = 0

        if (hits == 3 and hand_mvn == 0):
            print(hand_mvn)
            f.seek(0)
            f.write('REP\n')
            f.truncate()

        elif (hits == 3 and hand_mvn == 1):
            print(hand_mvn)
            state = get_state(state, f, +1)               

        elif (hits == 3 and hand_mvn == 2) :
            print(hand_mvn)
            state = get_state(state, f, -1)               

        elif (hits == 3 and hand_mvn == 3) :
            print(hand_mvn)
            f.seek(0)
            f.write('FIST\n')
            f.truncate()

        last_predict = hand_mvn 

    return 0



def classification(used_samples, model):
    # TODO: Conexion con el arduino, lectura de used samples 
    # hacer una "libreria que me devuelva resultados" y otra para inyectarselos algo concurrente (?)
    
    f = open("D:\\PROYECTO_MANO_FPGA\\GIT\\python\\3D\\com.txt", "w")
    state = ''

    online, port = arduino.serial_connection()
    n_samples = 256
    hits = 0
    last_predict = 0
    input('THE MODEL IS READY TO CLASSIFY, PLS PRESS ENTER TO CONNECT TO THE ARDUINO AND BEGIN')

    while True:
        samples = arduino.read_samples(port, n_samples, 2)

        ch1rms, ch2rms = int (np.round(np.sqrt(np.mean(samples[0]**2)))), int (np.round(np.sqrt(np.mean(samples[0]**2))))    
        
        hand_mvn = model.predict([ch1rms, ch2rms])[0]
        print(hand_mvn)

        if last_predict == hand_mvn:
            hits += 1
        else:
            hits = 0

        if (hits == 3 and hand_mvn == 0 and state != 'REP'):
            print(hand_mvn)
            #keyboard.release("right")
            #keyboard.release("left")
            #keyboard.release("z")
            
            state = 'REP'
            f.seek(0)
            f.write('REP\n')
            f.truncate()

        elif (hits == 3 and hand_mvn == 1 and state != 'FLEX'):
            print(hand_mvn)
            #keyboard.press("right")
            state = 'FLEX'
            f.seek(0)
            f.write('FLEX\n')
            f.truncate()
                
        elif (hits == 3 and hand_mvn == 2  and state != 'EXT') :
            print(hand_mvn)
            #keyboard.press("left")
            state = 'EXT'
            f.seek(0)
            f.write('EXT\n')
            f.truncate()

        elif (hits == 3 and hand_mvn == 3  and state != 'FIST') :
            print(hand_mvn)
            #keyboard.press("z")
            state = 'FIST'
            f.seek(0)
            f.write('FIST\n')
            f.truncate()

        last_predict = hand_mvn 

    return 0
