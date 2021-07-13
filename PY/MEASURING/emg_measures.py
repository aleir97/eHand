import serial
import winsound
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt

def save_csv(A1, A2, file):
    data = {'CH1': A1,
            'CH2': A2}

    df = pd.DataFrame(data, columns= ['CH1', 'CH2'])
    path = r'D:\PROYECTO_MANO_FPGA\GIT\PY\\' + file + '.csv' 
    df.to_csv (path, index = False, header=True)

def make_sound():
    #Sound parameters
    frequency = 500  # Set Frequency To 2500 Hertz
    duration = 2000  # Set Duration To 1000 ms == 1 second
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

def main():
    # Serial port connection
    port = serial.Serial('COM3', baudrate=115200, timeout=0.5) # Establish connection with arduino
    port.setDTR(False)
    time.sleep(1)
    port.flushInput()
    port.setDTR(True)

    sampleRate = 1000
    n = np.arange(1, sampleRate+1)
    med = 0
    med_type = ''

    while True:
        med_type = input('**** PROGRAM TO READ EMG SAMPLES FROM SERIAL PORT AND CONVERT TO CSV: ****' +
                            '\n (1) resting \n (2) flexion \n (3) extension \n (4) fist \n (e)xit \n')

        if med_type == 'e':
            exit()
        elif med_type == '1':
            med_type = 'rest'
        elif med_type == '2':
            med_type = 'flex'
        elif med_type == '3':
            med_type = 'ext'
        elif med_type == '4':
            med_type = 'fist'

        A1 = []
        A2 = []
        med += 1
        
        make_sound()
        
        # Send the signal sync to arduino
        port.write(bytes(b'ini'))

        # Receiving signal sync from arduino 
        for i in range(100):
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

        A1= list(map(int,A1))
        A2= list(map(int,A2))
        
        plot_measures(n, A1, A2)
       
        file = med_type + str(med)
        save_csv(A1, A2, file)

if __name__ == "__main__":
    main()



