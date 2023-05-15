'''
	- Python module	to plot	information	from a serial device
	
	Copyright (C) 2021 Alejandro Iregui	Valcarcel

	This program is	free software: you can redistribute	it and/or modify
	it under the terms of the GNU General Public License as	published by
	the	Free Software Foundation, either version 3 of the License, or
	(at	your option) any later version.

	This program is	distributed	in the hope	that it	will be	useful,
	but	WITHOUT	ANY	WARRANTY; without even the implied warranty	of
	MERCHANTABILITY	or FITNESS FOR A PARTICULAR	PURPOSE.  See the
	GNU	General	Public License for more	details.

	You	should have	received a copy	of the GNU General Public License
	along with this	program.  If not, see <https://www.gnu.org/licenses/>.
'''

from matplotlib.animation import FuncAnimation
import numpy as	np
import matplotlib.pyplot as	plt	
import matplotlib as mpl
mpl.use('MacOSX')
import com.arduino as arduino

class EmgPlot:
	def	__init__(self, axs, port, n_samples, channels):		
		self.axs = axs

		for x, i in zip(self.axs, range(channels)) : x.set_title(F"CH{i+1}: ")
		for x in self.axs : x.grid(True), x.set(xlim=(0, n_samples), ylim=(-500, 500))
		self.lines = [x.plot(np.arange(n_samples), np.zeros(n_samples), 'k-') for x in self.axs]

		self.port = port
		self.n_samples = n_samples	
		self.channels = channels

	def	__call__(self, i):
		samples	= arduino.read_samples(self.port, self.n_samples, self.channels)
		for i in range(samples.shape[0]):
			self.lines[i][0].set_ydata(samples[i])


def plot_emg(n_samples, channels):
	_ , port = arduino.serial_connection()

	fig, axs = plt.subplots(channels) 
	axs = axs if channels > 1 else [axs]
	emg_plot = EmgPlot(axs, port, n_samples, channels)
	anim = FuncAnimation(fig, emg_plot, interval=150)
	plt.show()
