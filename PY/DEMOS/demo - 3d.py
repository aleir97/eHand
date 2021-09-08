import serial
import winsound
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt
import mouse

def main():
    f = open("D:\\PROYECTO_MANO_FPGA\\GIT\\PY\\3D\\com.txt", "w")
    state = ''

    # Serial port connection
    port = serial.Serial('COM3', baudrate=115200, timeout=0.5) # Establish connection with arduino
    port.setDTR(False)
    time.sleep(1)
    port.flushInput()
    port.setDTR(True)

    sampleRate = 256
    n = np.arange(1, sampleRate+1)
    med = 0
    med_type = ''

    input()
    while True:
        # Send the signal sync to arduino
        port.write(bytes(b'ini'))
        
        # Receiving signal sync from arduino 
        for i in range(10):
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

                A1=np.fromiter(map(int, A1), dtype=int) 
                
                rms = int (np.round(np.sqrt(np.mean(A1**2))))
                #rms = np.mean(A1)

                if(rms > 200 and state != 'EXT' ):
                    state = 'EXT'
                    f.seek(0)
                    f.write('EXT\n')
                    f.truncate()
                    time.sleep(0.25)
                elif (rms < 200 and state != 'STOP'):
                    state = 'STOP'
                    f.seek(0)
                    f.write('STOP\n')
                    f.truncate()
                    time.sleep(0.25)


                print(rms)
                #time.sleep(2)

        else:
            port.write(bytes(b'stop'))    
 
if __name__ == "__main__":
    main()



