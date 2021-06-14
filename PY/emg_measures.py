import serial
import winsound
import numpy as np
import time
import pandas as pd

sampleRate = 1000

port = serial.Serial('COM5', baudrate=115200, timeout=1.0) # Establish connection with arduino
port.setDTR(False)
time.sleep(1)
port.flushInput()
port.setDTR(True)

med = 0
while input('**** PROGRAM TO READ EMG SAMPLES FROM SERIAL PORT AND CONVERT TO CSV: ****\n (e)xit \n enter \n') != 'e':
    A1 = []
    A2 = []
    med += 1
    
    frequency = 500  # Set Frequency To 2500 Hertz
    duration = 2000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

    # Send the signal sync to arduino
    port.write(bytes(b'ini'))

    # Receiving signal sync from arduino 
    for i in range(100):
        line = port.readline().decode('ascii')
        if line == 'ini\r\n':
            break

    if line == 'ini\r\n':
        for i in range(sampleRate):
            #print('LECTURA A1:', port.readline().decode('ascii'))
            #print('LECTURA A2:', port.readline().decode('ascii'))
            A1.append(port.readline().decode('ascii'))
            A2.append(port.readline().decode('ascii'))

    else:
        print('NO LEÍ EL INI :(')
        exit()
    
    A1= np.asarray(A1)
    A2= np.asarray(A2)

    data = {'CH1': A1,
            'CH2': A2}

    df = pd.DataFrame(data, columns= ['CH1', 'CH2'])
    path = r'D:\PROYECTO_MANO_FPGA\GIT\PY\med' + str(med) + '.csv' 
    df.to_csv (path, index = False, header=True)

    port.write(bytes(b'stop'))







