from measuring.measuring import *
from analysis.emg_analysis import *
from utils.StoppableThread import *

import serial
import serial.tools.list_ports
import PySimpleGUI as sg
from subprocess import Popen
import time


def serial_connection():
    # Serial port connection
	found = False
	ports = list(serial.tools.list_ports.grep('.*Arduino.*', include_links=False))

	if len(ports) != 0:
		found = True	
	else:
		sg.popup_error('Connection not found, going offline')
		return False, None

	if found == True:
		try:
			port = serial.Serial(ports[0][0], baudrate=115200, timeout=1) # Establish connection with arduino
			return True, port 

		except:
			sg.popup_error('Error at the connection, going offline') 
			return False, None


def offline_events(window, event, values):
	if event == "-FOLDER-":
		folder = values['-FOLDER-']  
		if folder != '':
			analysis(folder)
        
	# To close the window
	elif (event == "EXIT" or event == sg.WIN_CLOSED): 
		window.close()
		exit()

	else:
		#TODO: interesante que el programa deje pasar de modo ofline a online
		sg.popup_error('Connect a device and restart the program') 

			
th = None
med = 0
p1 = None

def online_events(window, event, values, port):
	global 	th 
	global	med
	global	p1

	if event == "MAKE MEASURE":
		med += 1
		make_measures(values['name_file'], port, 1000, med)

	elif event == "-FOLDER-":
		folder = values['-FOLDER-']  
		if folder != '':
			analysis(folder)

	elif event == "REAL TIME PLOT": 
		port.close()
		p1 = Popen("py D:\\PROYECTO_MANO_FPGA\\GIT\\python\\analysis\\plot.py", shell = True)

	elif event == "STOP THE PLOT!":
		if p1 != None:
			Popen("TASKKILL /F /PID {pid} /T".format(pid=p1.pid))
			time.sleep(2)
			port.open()
			p1 = None
        
	elif event == "PLAY!":
		treshold = 9999 if values['treshold'] == '' else int(values['treshold'])

		th = StoppableThreadGame(port, treshold)
		th.start()

	elif event == "CONNECT 3D!":
		treshold = 9999 if values['treshold'] == '' else int(values['treshold'])

		th = StoppableThreadModel(port, treshold)
		th.start()
            
	elif event ==  "STOP!":
		if th != None:
			port.write(bytes(b's'))    
			th.raise_exception()
			th.join()
			th = None
            
	# To close the window
	elif (event == "EXIT" or event == sg.WIN_CLOSED): 
		if th != None:
			port.write(bytes(b's'))    
			th.raise_exception()
			th.join()
			th = None

		if p1 != None:
			Popen("TASKKILL /F /PID {pid} /T".format(pid=p1.pid))
			time.sleep(2)
			p1 = None
    
		window.close()
		exit()

def main():
	online, port = serial_connection()		

	#TODO: separar la generacion de UI como componente
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
		
		if online:
			online_events(window, event, values, port)
		else:
			offline_events(window, event, values)


if __name__ == "__main__":
	main()


