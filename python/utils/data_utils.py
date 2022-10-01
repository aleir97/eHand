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
import matplotlib.pyplot as plt
import serial
import time


root_path = r'D:\PROYECTO_MANO_FPGA\GIT\python\models'

def generate_dataset(samples):
    read_path = root_path+ '\\dataset'
    ind =-1
    
    for entry in os.scandir(read_path):
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
                df = df.append(df2, ignore_index= True)

    path = dataset_path+ 'emg_data.csv' 
    df.to_csv(path, index = False, header=True)    

def get_data(used_samples):
    # Function to generate the data
	generate_dataset(used_samples)

	path = root_path+ '\\emg_data.csv'
	data_csv = pd.read_csv(path)

	data = np.dstack((data_csv["CH1"].to_numpy(), data_csv["CH2"].to_numpy()))
	data = data.reshape(data.shape[1:])	

	targets = data_csv['class'].to_numpy()

	return data, targets

def classification(used_samples, model):
    # TODO: Conexion con el arduino, lectura de used samples 
    # hacer una "libreria que me devuelva resultados" y otra para inyectarselos algo concurrente (?)
    
    f = open("D:\\PROYECTO_MANO_FPGA\\GIT\\python\\3D\\com.txt", "w")
    state = ''

    # Serial port connection
    port = serial.Serial('COM3', baudrate=115200, timeout=0.5) # Establish connection with arduino
    port.setDTR(False)
    time.sleep(1)
    port.flushInput()
    port.setDTR(True)
    
    A1 = []
    A2 = []
    hits = 0
    last_predict = 0
    input('THE MODEL IS READY TO CLASSIFY, PLS PRESS ENTER TO CONNECT TO THE ARDUINO AND BEGIN')
    while True:
        # Send the signal sync to arduino
        port.write(bytes(b'ini'))
        
        # Receiving signal sync from arduino 
        for i in range(50):
            time.sleep(0.005)
            line = port.readline().decode('ascii')
            if line == 'ini\r\n':
                break
        
        if line == 'ini\r\n':
            while True:
                A1 = []
                A2 = []
                for i in range(used_samples):
                    A1.append(port.readline().decode('ascii'))
                    A2.append(port.readline().decode('ascii'))
                    
                A1=np.fromiter(map(int, A1), dtype=int) 
                A2=np.fromiter(map(int, A2), dtype=int)

                ch1rms, ch2rms = int (np.round(np.sqrt(np.mean(A1**2)))), int (np.round(np.sqrt(np.mean(A2**2))))    
                
                #print("RMS CH1:%d, CH2:%d\n" % (ch1rms, ch2rms))
                hand_mvn = model.predict([ch1rms, ch2rms])[0]
                
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
        else:
            port.write(bytes(b'stop'))  


    return 0
