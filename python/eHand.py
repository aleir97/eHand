from measuring.measuring import *
from analysis.emg_analysis import *
from utils.StoppableThread import *

import serial
import serial.tools.list_ports
import PySimpleGUI as sg
from subprocess import Popen
import time


def serial_connection():
	#TODO: Que te deje elegir la conexion mediante una lista de dispositivos
    # Serial port connection
	found = False
	ports = list(serial.tools.list_ports.grep('.*Arduino.*', include_links=False))

	if len(ports) != 0:
		found = True	
	else:
		sg.popup_error('\n\n       Connection not found, going offline       \n\n')
		return False, None

	if found == True:
		try:
			port = serial.Serial(ports[0][0], baudrate=115200, timeout=1) # Establish connection with arduino
			return True, port 

		except:
			sg.popup_error('\n\n       Error at the connection, going offline       \n\n') 
			return False, None


def offline_events(window, event, values):
	if event == 'ANALYZE':
		ui_analysis()
        
	# To close the window
	elif (event == "EXIT" or event == sg.WIN_CLOSED): 
		window.close()
		exit()

	else:
		#TODO: interesante que el programa deje pasar de modo ofline a online
		sg.popup('\n\n       Connect a device and restart the program       \n\n') 

			
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

	elif event == 'ANALYZE':
		ui_analysis()

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

def ui_analysis():
	layout = [[sg.Text('File analysis:'), sg.In(enable_events=True, key='-FOLDER-', visible=False), sg.FilesBrowse('Add Files', target='-FOLDER-'),
			   sg.Column([[sg.Checkbox('Mean', default=False, key='Mean')],
              [sg.Checkbox('RMS',  default=False, key= 'RMS')],
              [sg.Checkbox('Fourier Transform', default=False, key= 'FFT')]])],
			  [sg.Button('Analyze', pad= (100, 10))],
              [sg.Exit('Exit')]]	

	window = sg.Window('Analysis', layout)

	files = []
	while True:
		event, values = window.read()
		
		if event == '-FOLDER-':
			# Meterle los valores de los checks
			files = files + values['-FOLDER-'].split(';')			

		elif event == 'Analyze':
			if len(values['-FOLDER-']) == 0:
				sg.popup('\n\n       Select some files       \n\n')
			else:
				analysis(files, [values['Mean'], values['RMS'], values['FFT']]) 
				files = []

		# To close the window
		elif (event == 'Exit' or event == sg.WIN_CLOSED): 
			break

	window.close()	


def ui_gen():
    # Window configuration
	sg.theme('DarkTeal9')
	layout = [[sg.Text('Insert the name of the record file:')],
            [sg.Input(key='name_file', size=(10,1)), sg.Button('MAKE MEASURE'), sg.Button('REAL TIME PLOT'),sg.Button('STOP THE PLOT!')],
            [[sg.In(enable_events=True, key='-FOLDER-', visible=False), sg.Button('ANALYZE DATA', key='ANALYZE')]], 
            [sg.Text("Treshold for the game or 3d Model:"), sg.Input(key='treshold',size=(10,1)), sg.Button('PLAY!'), sg.Button('CONNECT 3D!'), sg.Button('STOP!')],
            [ sg.Exit('EXIT')]]

	return sg.Window("eHand", layout)
   

def main():
	online, port = serial_connection()		

	window = ui_gen()	

	# Create an event loop
	while True:
		event, values = window.read()
		
		if online:
			online_events(window, event, values, port)
		else:
			offline_events(window, event, values)


if __name__ == "__main__":
	main()


