'''
    - Python control demo to interface the EMG and system's mouse left-click
    
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
import mouse
import os
import time
import com.arduino as arduino

def game(port, treshold):
	os.system("start \"\" https://www.minijuegos.com/juego/the-sniper-code")
	n_samples = 256    
    
    
	samples = arduino.read_samples(port, n_samples, 1)

	while True:

		rms = int (np.round(np.sqrt(np.mean(samples**2))))

		if(rms > treshold ):
			mouse.click('left')
			print(rms)






