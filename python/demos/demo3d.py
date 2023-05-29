'''
    - Python control demo to interface the EMG and the 3D Blender scripts
    
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
import time
import threading 
# This is needed till the execution of models is at eHand
import sys
sys.path.insert(1, '/Users/aleir97/Documents/eHand/python/')
import com.arduino as arduino
from utils.path_handler import blender_dir 


f = open("/Users/aleir97/Documents/eHand/python/3D/com.txt", "w")
# f = open(blender_dir / "com.txt", "w")

def model(port, treshold):
    state = ''
    n_samples = 256

    while True:
        samples = arduino.read_samples(port, n_samples, 2)
        rms = int (np.round(np.sqrt(np.mean(samples[0]**2))))

        if (rms > treshold and state != 'FIST' ):
            state = 'FIST'
            f.seek(0)
            f.write('FIST\n')
            f.truncate()
            time.sleep(0.005)

        elif (rms < treshold and state != 'REP'):
            state = 'REP'
            f.seek(0)
            f.write('REP\n')
            f.truncate()
            time.sleep(0.005)

        print(rms)

# TODO: Make a Control class for the different classification methods, such as treshold, svm or nnet
from enum import IntEnum, auto
class pose_states(IntEnum):
    EXT   = 0
    FLEX  = auto()
    NEY   = auto()
    PEACE = auto()
    ROCK  = auto()
    SEÑ   = auto()
    END   = auto()

def get_state(pose, com_fl, order):
    if pose == pose_states.EXT:
        com_fl.seek(0)
        com_fl.write('EXT\n')
        com_fl.truncate()
        return (pose+order) 

    if pose == pose_states.FLEX:
        com_fl.seek(0)
        com_fl.write('FLEX\n')
        com_fl.truncate()
        return (pose+order) 

    if pose == pose_states.NEY:
        com_fl.seek(0)
        com_fl.write('NEY\n')
        com_fl.truncate()
        return (pose+order) 

    if pose == pose_states.PEACE:
        com_fl.seek(0)
        com_fl.write('PEACE\n')
        com_fl.truncate()
        return (pose+order) 

    if pose == pose_states.ROCK:
        com_fl.seek(0)
        com_fl.write('ROCK\n')
        com_fl.truncate()
        return (pose+order) 

    if pose == pose_states.SEÑ:
        com_fl.seek(0)
        com_fl.write('SEÑ\n')
        com_fl.truncate()
        return (pose+order) 

def classification_state_machine(n_samples, model):
    # TODO: Conexion con el arduino, lectura de used samples 
    # hacer una "libreria que me devuelva resultados" y otra para inyectarselos algo concurrente (?)
    
    state = pose_states.EXT   

    online, port = arduino.serial_connection()
    hits = 0
    last_predict = 0
    input('THE MODEL IS READY TO CLASSIFY, PLS PRESS ENTER TO CONNECT TO THE ARDUINO AND BEGIN')

    while True:
        samples = arduino.read_samples(port, n_samples, 2)

        ch1rms, ch2rms = int (np.round(np.sqrt(np.mean(samples[0]**2)))), int (np.round(np.sqrt(np.mean(samples[1]**2))))    
    
        hand_mvn = model.predict([ch1rms, ch2rms])[0]
        # print(hand_mvn)

        if last_predict == hand_mvn:
            hits += 1
        else:
            hits = 0

        if (hits >= 2 and hand_mvn == 0):
            print(hand_mvn)
            f.seek(0)
            f.write('REP\n')
            f.truncate()

        elif (hits >= 2 and hand_mvn == 1):
            print(hand_mvn, state)
            state = get_state(state, f, +1) % pose_states.END             

        elif (hits >= 2 and hand_mvn == 2) :
            print(hand_mvn, state)
            state = get_state(state, f, -1) % pose_states.END             

        elif (hits >= 3 and hand_mvn == 3) :
            print(hand_mvn)
            f.seek(0)
            f.write('FIST\n')
            f.truncate()

        last_predict = hand_mvn 

    return 0

def classification(n_samples, port, model):
    state = ''

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
