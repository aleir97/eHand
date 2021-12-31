import winsound
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import os
from datetime import datetime
import time


date = datetime.today().strftime('%d-%Y-%m')
measure_dir =  r'D:\PROYECTO_MANO_FPGA\GIT\measures'+ '\\'+ date

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

def plot_measures(n, A1, A2):
    plt.figure()
    ax = plt.subplot(211)
    ax.set_title("CH1:")
    plt.plot(n, A1)

    ax = plt.subplot(212)
    ax.set_title("CH2:")
    plt.plot(n, A2)
    plt.show()

def make_measures(namefl, port, sampleRate, med):
    med_type = ''
    n = np.arange(1, sampleRate+1)

    med_type = namefl

    if med_type == 'exit':
        exit()
    
    A1 = []
    A2 = []
    
    make_sound()

    # Send the signal sync to arduino
    port.write(bytes(b'ini'))
    
    # Receiving signal sync from arduino 
    for i in range(50):
        time.sleep(0.005)
        line = port.readline().decode('ascii')
        if line == 'ini\r\n':
            break

    if line == 'ini\r\n':
        for i in range(sampleRate):
            #print('MEASURE A1:', port.readline().decode('ascii'))
            #print('MEASURE A2:', port.readline().decode('ascii'))
            A1.append(port.readline().decode('ascii'))
            A2.append(port.readline().decode('ascii'))

    else:
        print('NO LEÍ EL INI :(')
        exit()

    port.write(bytes(b'stop'))

    A1= list(map(int, A1))
    A2= list(map(int, A2))
    
    plot_measures(n, A1, A2)

    file = med_type + str(med)
    save_csv(A1, A2, file)

    port.write(bytes(b'stop'))    
