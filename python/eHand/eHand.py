import sys 
import os

from PySimpleGUI.PySimpleGUI import No
sys.path.append(os.path.abspath("D:\PROYECTO_MANO_FPGA\GIT\python\MEASURING"))
from measuring import make_measures

sys.path.append(os.path.abspath("D:\PROYECTO_MANO_FPGA\GIT\python\ANALYSIS"))
from emg_analysis import analysis

sys.path.append(os.path.abspath("D:\PROYECTO_MANO_FPGA\GIT\python\DEMOS"))
from plot import plot

sys.path.append(os.path.abspath("D:\PROYECTO_MANO_FPGA\GIT\python\DEMOS"))
from game import game
from demo3d import model 

import matplotlib.animation as animation
import serial
import PySimpleGUI as sg
import threading 
import ctypes
from subprocess import Popen
import time

class StoppableThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
          
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


class StoppableThreadGame(StoppableThread):
    def __init__(self, port, treshold):
        StoppableThread.__init__(self)
        self.port = port
        self.treshold = treshold

    def run(self):
        # target function of the thread class
        try:        
            game(self.port, self.treshold)
        
        finally:
            print('ended')

class StoppableThreadModel(StoppableThread):
    def __init__(self, port, treshold):
        StoppableThread.__init__(self)
        self.port = port
        self.treshold = treshold

    def run(self):
        # target function of the thread class
        try:        
            model(self.port, self.treshold)
        
        finally:
            print('ended')


def main():
    # Serial port connection
    port = serial.Serial('COM3', baudrate=115200, timeout=1) # Establish connection with arduino
    th = None
    med = 0
    p1 = None
    
    # Window configuration
    sg.theme('DarkTeal9')
    layout = [[sg.Text("Insert the name of the record file:")],
            [sg.Input(key='name_file', size=(10,1)), sg.Button("MAKE MEASURE"), sg.Button("REAL TIME PLOT"),sg.Button("STOP THE PLOT!")],
            [[sg.In(enable_events=True, key='-FOLDER-', visible=False), sg.FolderBrowse("ANALYZE DATA", target='-FOLDER-')]], 
            [sg.Text("Treshold for the game or 3d Model:"), sg.Input(key='treshold',size=(10,1)), sg.Button("PLAY!"), sg.Button("CONNECT 3D!"), sg.Button("STOP!")],
            [ sg.Exit("EXIT")]]

    window = sg.Window("eHand", layout)
   
    # Create an event loop
    while True:
        event, values = window.read()
        
        if event == "MAKE MEASURE":
            med += 1
            make_measures(values['name_file'], port, 1000, med)

        if event == "REAL TIME PLOT": 
            port.close()
            p1 = Popen("py D:\\PROYECTO_MANO_FPGA\\GIT\\python\\analysis\\plot.py", shell = True)

        if event == "STOP THE PLOT!":
            if p1 != None:
                Popen("TASKKILL /F /PID {pid} /T".format(pid=p1.pid))
                time.sleep(2)
                port.open()

        if event == "-FOLDER-":
            folder = values['-FOLDER-']  
            analysis(folder)
        
        if event == "PLAY!":
            if values['treshold'] == '':
                treshold = 9999
            else:    
                treshold = int(values['treshold'])

            th = StoppableThreadGame(port, treshold)
            th.start()

        if event == "CONNECT 3D!":
            if values['treshold'] == '':
                treshold = 9999
            else:    
                treshold = int(values['treshold'])

            th = StoppableThreadModel(port, treshold)
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
                th.raise_exception()
                th.join()

            if p1 != None:
                Popen("TASKKILL /F /PID {pid} /T".format(pid=p1.pid))
                time.sleep(2)
    
            window.close()
            break    

        elif event == sg.WIN_CLOSED:
            if th != None:
                port.write(bytes(b's'))    
                th.raise_exception()
                th.join()

            if p1 != None:
                Popen("TASKKILL /F /PID {pid} /T".format(pid=p1.pid))
                time.sleep(2)

            window.close()
            break

if __name__ == "__main__":
    main()


