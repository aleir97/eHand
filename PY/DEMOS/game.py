import numpy as np
import mouse
import threading 

def game(port, treshold):
   
    sampleRate = 256    
    # Send the signal sync to arduino
    port.write(bytes(b'ini'))
    
    # Receiving signal sync from arduino 
    for i in range(10):
        line = port.readline().decode('ascii')
        if line == 'ini\r\n':
            break
    
    if line == 'ini\r\n':
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            A1 = []
            for i in range(sampleRate):
                #print('MEASURE A1:', port.readline().decode('ascii'))
                #print('MEASURE A2:', port.readline().decode('ascii'))
                A1.append(port.readline().decode('ascii'))
                port.readline()

            A1=np.fromiter(map(int, A1), dtype=int) 
            
            rms = int (np.round(np.sqrt(np.mean(A1**2))))
            #mean = np.mean(A1)

            if(rms > treshold ):
                mouse.click('left')

            print(rms)
        print('HOLAAA')
        exit()    
    else:
        port.write(bytes(b's'))    





