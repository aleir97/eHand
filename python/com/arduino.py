'''
    - Python module to synchronize between serial device and PC to acquire and measure EMG samples
    
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

import numpy as np
import time
import serial
import serial.tools.list_ports


def serial_connection():
	#TODO: Que te deje elegir la conexion mediante una lista de dispositivos
    # Serial port connection
	found = False
	ports = list(serial.tools.list_ports.grep('cu.usbmodem11201', include_links=False))

	if len(ports) != 0:
		found = True	
	else:
		return False, None

	if found == True:
		try:
			port = serial.Serial(ports[0][0], baudrate=115200, timeout=1) # Establish connection with arduino
			time.sleep(5)
			return True, port 

		except:
			return False, None

def read_samples(port, n_samples, channels):
	serial_sync_fl = b'\xaa'
	serial_end_fl  = b'\xbb'
	samples = np.zeros(channels*n_samples, dtype=int)
	cont = 0

	port.flush()
    # Send the sync signal to the arduino
	port.write(serial_sync_fl)

    # Receiving sync signal from arduino 
	while (port.readable() and port.read()!= serial_sync_fl):
		cont +=1
		time.sleep(0.001)
		if cont == 1000:
			raise Exception("Could not sync with Arduino")

	for i in range(n_samples*channels):
		samples[i] = port.readline().decode('ascii')

	port.write(bytes(serial_end_fl))
	time.sleep(0.100)
	port.write(bytes(serial_end_fl))

	samples = np.reshape(samples, (channels, n_samples), order='F')

	return samples