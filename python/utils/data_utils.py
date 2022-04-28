import numpy as np
import pandas as pd
import os 

dataSet_path = r'D:\PROYECTO_MANO_FPGA\GIT\python\models'

def generate_dataset(samples):
    dataSet_dire = dataSet_path+ '\\dataset'
    ind =-1
    for entry in os.scandir(dataSet_dire):
        if (entry.is_file()):
            ind += 1
            
            signal = pd.read_csv(entry.path)
            
            ch1, ch2 = signal["CH1"].to_numpy(), signal["CH2"].to_numpy()    
            ch1, ch2  = ch1[1:samples+1], ch2[1:samples+1] 
        
            ch1rms, ch2rms = int (np.round(np.sqrt(np.mean(ch1**2)))), int (np.round(np.sqrt(np.mean(ch2**2))))         
            
            #print("DATA FROM FILE: "+ entry.name)
            #print("RMS CH2 VAL:"+ str(ch1rms))
            #print("RMS CH2 VAL:"+ str(ch2rms))

            if "rest" in entry.name:
                mvmnt = 0
            elif 'flex'  in entry.name:
                mvmnt = 1 
            elif 'ext' in entry.name:
                mvmnt = 2
            elif 'fist' in entry.name:
                mvmnt = 3

            data = {'CH1': ch1rms,
            'CH2': ch2rms,
            'class': mvmnt    
            }

            if (ind == 0):
                 df = pd.DataFrame(data, columns= ['CH1', 'CH2', 'class'], index = [ind])

            else:
                df2 = pd.DataFrame(data, columns= ['CH1', 'CH2', 'class'], index = [0]) 
                df = df.append(df2, ignore_index= True)

    path = r'D:\PROYECTO_MANO_FPGA\GIT\python\models\\'+ 'dataSet'+ '.csv' 
    df.to_csv(path, index = False, header=True)    