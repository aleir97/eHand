'''
    - Python control demo to interface the EMG and system's mouse left-click
    
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
import mouse
import os
import time

def game(port, treshold):
    os.system("start \"\" https://www.minijuegos.com/juego/the-sniper-code")
    sampleRate = 256    

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
            for i in range(sampleRate):
                #print('MEASURE A1:', port.readline().decode('ascii'))
                #print('MEASURE A2:', port.readline().decode('ascii'))
                A1.append(port.readline().decode('ascii'))
                port.readline()

            A1 = np.fromiter(map(int, A1), dtype=int) 
            
            rms = int (np.round(np.sqrt(np.mean(A1**2))))

            if(rms > treshold ):
                mouse.click('left')

            print(rms)

    else:
        port.write(bytes(b's'))    





