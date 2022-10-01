'''
    - Python module to plot information from a serial device
    
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
import matplotlib.pyplot as plt 
import serial
import time

def plot():
    # Serial port connection
    port = serial.Serial('COM3', baudrate=115200, timeout=1) # Establish connection with arduino
    
    time.sleep(3)

    sampleRate = 256
    n = np.arange(1, sampleRate+1)

    plt.figure()
    ax = plt.subplot(211)
    ax.set_title("CH1:")
    ax = plt.subplot(212)
    ax.set_title("CH2:")
    
    #plt.show()
    
    # Send the signal sync to arduino
    port.write(bytes(b'ini'))
    
    # Receiving signal sync from arduino 
    for i in range(20):
        line = port.readline().decode('ascii')
        if line == 'ini\r\n':
            break
    
    if line == 'ini\r\n':
        while True:
             
            A1 = []
            A2 = []

            plt.clf()
            for i in range(sampleRate):
                #print('MEASURE A1:', port.readline().decode('ascii'))
                #print('MEASURE A2:', port.readline().decode('ascii'))
                A1.append(port.readline().decode('ascii'))
                A2.append(port.readline().decode('ascii'))

            A1= list(map(int, A1))
            A2= list(map(int, A2))
            
            plt.plot(n, A1)
            plt.plot(n, A2)
            plt.pause(0.001)
            

    else:
        port.write(bytes(b's'))    


def main():
    plot()

if __name__ == "__main__":
    main()

