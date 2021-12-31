import numpy as np
import time
import threading 

def model(port, treshold):
    f = open("D:\\PROYECTO_MANO_FPGA\\GIT\\python\\3D\\com.txt", "w")
    state = ''
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

            A1 = np.fromiter(map(int, A1), dtype=int) 
            
            rms = int (np.round(np.sqrt(np.mean(A1**2))))

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

    else:
        port.write(bytes(b'stop'))    
        exit()
    
