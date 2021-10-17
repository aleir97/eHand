import sys 
import os
sys.path.append(os.path.abspath("D:\PROYECTO_MANO_FPGA\GIT\py\MEASURING"))
from measuring import make_measures

sys.path.append(os.path.abspath("D:\PROYECTO_MANO_FPGA\GIT\py\ANALYSIS"))
from emg_analysis import analysis

sys.path.append(os.path.abspath("D:\PROYECTO_MANO_FPGA\GIT\py\DEMOS"))
from game import game
from demo3d import model 

import serial
import PySimpleGUI as sg
import threading 

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self.do_run = True

def main():
    # Serial port connection
    port = serial.Serial('COM3', baudrate=115200, timeout=0.5) # Establish connection with arduino
    th = None

    # Window configuration
    sg.theme('DarkTeal9')
    layout = [[sg.Text("Insert the name of the record file:")],
            [sg.Input(key='name_file'), sg.Button("MAKE MEASURE")],
            [[sg.In(enable_events=True, key='-FOLDER-', visible=False), sg.FolderBrowse("ANALYZE DATA", target='-FOLDER-')]], 
            [sg.Text("Treshold for the game or 3d Model:"), sg.Input(key='treshold',size=(10,1)), sg.Button("PLAY!"), sg.Button("CONNECT 3D!"), sg.Button("STOP!")],
            [ sg.Exit("EXIT")]]

    window = sg.Window("eHand", layout)
   
    # Create an event loop
    while True:
        event, values = window.read()
        
        if event == "MAKE MEASURE":
            make_measures(values['name_file'], port, 1000)

        if event == "-FOLDER-":
            folder = values['-FOLDER-']  
            analysis(folder)
        
        if event == "PLAY!":
            treshold = int(values['treshold'])

            th = StoppableThread(target=game, args=(port,treshold,))
            th.start()

        if event == "CONNECT 3D!":
            treshold = int(values['treshold'])

            th = StoppableThread(target=model, args=(port,treshold,))
            th.start()

        if event ==  "STOP!":
            if th != None:
                port.write(bytes(b's'))    
                th.do_run = False
                th.join(1)
                print(th.is_alive())

        # To close the window
        elif event == "EXIT": 
            if th != None:
                port.write(bytes(b's'))    
                th.do_run = False
                th.join(1)
  
            window.close()
            break    

        elif event == sg.WIN_CLOSED:
            if th != None:
                port.write(bytes(b's'))    
                th.do_run = False
                th.join(1)

            window.close()
            break

if __name__ == "__main__":
    main()


