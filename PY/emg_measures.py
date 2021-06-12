import serial
import os
import numpy as np
import time

sampleRate = 2000
A1 = []
A2 = []

port = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1.0) # Establish connection with arduino
port.setDTR(False)
time.sleep(1)
port.flushInput()
port.setDTR(True)

input('PROGRAM TO READ EMG SAMPLES FROM SERIAL PORT')

duration = 1  # seconds
freq = 500  # Hz
os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

# Send the signal sync to arduino
port.write(b'1')

line = port.readline().decode('ascii')
if line == 'ini\r\n':
    for i in range(sampleRate):
        #print('LECTURA A1:', port.readline().decode('ascii'))
        #print('LECTURA A2:', port.readline().decode('ascii'))
        A1.append(port.readline().decode('ascii'))
        A2.append(port.readline().decode('ascii'))

else:
    print('NO LEÍ EL INI :(')


A1= np.asarray(A1)
A2= np.asarray(A2)

A1_fl= open("A1.txt", "w")
for row in A1:
    A1_fl.write(row)
A1_fl.close()

A2_fl= open("A2.txt", "w")
for row in A2: 
     A2_fl.write(row)
A2_fl.close()







