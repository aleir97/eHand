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

