'''
  - Python eHand main program, user interface and module calls

	Copyright (C) 2021 Alejandro Iregui Valcarcel

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import sys
from utils.path_handler import ehand_path
sys.path.insert(1, ehand_path)

from measuring.measuring import *
from analysis.emg_analysis import *
from utils.StoppableThread import *
from analysis.plot import plot_emg
from utils.data_utils import get_data
from models.nnet import *
from demos.demo3d import classification, classification_state_machine

import PySimpleGUI as sg
import com.arduino as arduino
import multiprocessing

th = None
med = 0
port = None
online = False
files = []

def connect():
  global port
  global online

  online, port = arduino.serial_connection()

  if (not online):
    sg.popup_error('\n\n Connection not found, going offline \t\t\n\n')

def offline_events(window, event, values):
  global files

  if event == 'ANALYZE':
    ui_analysis()

  elif event == '-DATASET-':
    files = files + values['-DATASET-'].split(';')

  elif event == 'TRAIN!':
    if len(files) == 0:
      sg.popup('\n\n     First add a training dataset!     \n\n')
    else:
      train_valid_nnet(*get_data(files, 256), True)

  # To close the window
  elif (event == "EXIT" or event == sg.WIN_CLOSED):
    window.close()
    exit()

  else:
    #TODO: interesante que el programa deje pasar de modo ofline a online
    sg.popup('\n\n Connect a device and restart the program \n\n')

def online_events(window, event, values):
  global  th
  global  med
  global  port
  global  files

  if event == "MAKE MEASURE":
    med += 1
    make_measures(values['name_file']+str(med), port, 2, 1000)

  elif event == 'ANALYZE':
    ui_analysis()

  elif event == "REAL TIME PLOT":
    port.close()
    p = multiprocessing.Process(target=plot_emg,args=(1000, 2))
    p.start()
    p.join()
    connect()

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

  elif event == '-DATASET-':
    files = files + values['-DATASET-'].split(';')

  elif event == 'TRAIN!':
    if len(files) == 0:
      sg.popup('\n\n     First add a training dataset!     \n\n')
    else:
      train_valid_nnet(*get_data(files, 256), True)

  elif event == '-MODEL-':
    classification(256, port, load_model(values['-MODEL-']))

  # To close the window
  elif (event == "EXIT" or event == sg.WIN_CLOSED):
    if th != None:
      port.write(bytes(b's'))
      th.raise_exception()
      th.join()
      th = None

    window.close()
    exit()

def ui_gen():
  # Window configuration
  sg.theme('DarkTeal9')
  layout = [[sg.Text('Insert the name of the record file:')],
      [sg.Input(key='name_file', size=(10,1)), sg.Button('MAKE MEASURE'), sg.Button('REAL TIME PLOT')],
      [[sg.In(enable_events=True, key='-FOLDER-', visible=False), sg.Button('ANALYZE DATA', key='ANALYZE')]],
      [sg.Text("Treshold for the game or 3d Model:"), sg.Input(key='treshold',size=(10,1)), sg.Button('PLAY!'), sg.Button('CONNECT 3D!'), sg.Button('STOP!')],
      [sg.Text("Train your Classifier:"), sg.In(enable_events=True, key='-DATASET-', visible=False), sg.FilesBrowse('Add train dataset', target='-DATASET-'), sg.Button('TRAIN!'),
          sg.In(enable_events=True, key='-MODEL-', visible=False), sg.FileBrowse('LOAD & RUN!', target='-MODEL-')],
      [sg.Exit('EXIT')]]

  return sg.Window("eHand", layout)

def ui_analysis():
  layout = [[sg.Text('File analysis:'), sg.In(enable_events=True, key='-FOLDER-', visible=False), sg.FilesBrowse('Add Files', target='-FOLDER-'),
         sg.Column([[sg.Checkbox('Mean', default=False, key='Mean')],
        [sg.Checkbox('RMS',  default=False, key= 'RMS')],
        [sg.Checkbox('Fourier Transform', default=False, key= 'FFT')]])],
        [sg.Button('Analyze', pad= (100, 10))],
        [sg.Exit('Exit')]]

  window = sg.Window('Analysis', layout)

  while True:
    event, values = window.read()

    if event == '-FOLDER-':
      files = []
      # Meterle los valores de los checks
      files = files + values['-FOLDER-'].split(';')

    elif event == 'Analyze':
      if len(values['-FOLDER-']) == 0:
        sg.popup('\n\n     Select some files     \n\n')
      else:
        analysis(files, [values['Mean'], values['RMS'], values['FFT']])

    # To close the window
    elif (event == 'Exit' or event == sg.WIN_CLOSED):
      break

  window.close()

def main():
  global online

  connect()
  window = ui_gen()

  # Create an event loop
  while True:
    event, values = window.read()

    if online:
      online_events(window, event, values)
    else:
      offline_events(window, event, values)


if __name__ == "__main__":
  main()


