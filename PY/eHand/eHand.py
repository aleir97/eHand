import sys 
import os
sys.path.append(os.path.abspath("D:\PROYECTO_MANO_FPGA\GIT\py\MEASURING"))
from measuring import make_measures

sys.path.append(os.path.abspath("D:\PROYECTO_MANO_FPGA\GIT\py\ANALYSIS"))
from emg_analysis import analysis

import serial
import PySimpleGUI as sg

def main():
    # Serial port connection
    port = serial.Serial('COM3', baudrate=115200, timeout=0.5) # Establish connection with arduino

    # Window configuration
    sg.theme('DarkTeal9')
    layout = [[sg.Text("Insert the name of the record file:")],
            [sg.Input(key='name_file'), sg.Button("MAKE MEASURE")],
            [[sg.In(enable_events=True, key='-FOLDER-', visible=False), sg.FolderBrowse("ANALYZE DATA", target='-FOLDER-')]], 
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

        # To close the window
        elif event == "EXIT":  
            window.close()
            break    

        elif event == sg.WIN_CLOSED:
            window.close()
            break

if __name__ == "__main__":
    main()


