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
import ctypes

class StoppableThread(threading.Thread):
    def __init__(self, port, treshold, isgame):
        threading.Thread.__init__(self)
        self.port = port
        self.treshold = treshold
        self.isgame = isgame

    def run(self):
        # target function of the thread class
        try:
            if self.isgame:
                game(self.port, self.treshold)
            else:
                model(self.port, self.treshold)    
        finally:
            print('ended')
          
    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')


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

            th = StoppableThread(port, treshold, True)
            th.start()

            #th = StoppableThread(target=game, args=(port,treshold,))
            #th.start()

        if event == "CONNECT 3D!":
            treshold = int(values['treshold'])

            th = StoppableThread(port, treshold, False)
            th.start()
            
        if event ==  "STOP!":
            if th != None:
                port.write(bytes(b's'))    
                th.raise_exception()
                th.join()

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


