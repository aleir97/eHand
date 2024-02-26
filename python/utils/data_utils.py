'''
  - Python utils module to work as interface between other modules

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
import pandas as pd

import pywt
from utils.path_handler import models_dir

def get_data(files, samples=256, channels=2):
  targets = []
  data = None

  for entry in files:
    path = entry if entry.path is None else entry.path
    print("DATA FROM FILE: "+ path)
    signal = pd.read_csv(path)

    ch1, ch2 = signal["CH1"].to_numpy(), signal["CH2"].to_numpy()
    # Extract 0HZ frequency info
    ch1, ch2 = ch1 - ch1.mean(), ch2 - ch2.mean()
    ch1, ch2  = ch1[1:samples+1], ch2[1:samples+1]

    if "rest" in path:
      targets.append(0)
    elif 'flex'  in path:
      targets.append(1)
    elif 'ext' in path:
      targets.append(2)
    elif 'fist' in path:
      targets.append(3)

    data = np.stack((ch1, ch2)) if data is None else np.concatenate((data, np.stack((ch1, ch2))))
  return data.reshape((data.shape[0]//channels, channels, -1)), np.array(targets)


def calculate_cwt(data, sampling_rate=1000, num_scales=56):
  # Define parameters
  nyquist_frequency = sampling_rate / 2  # Nyquist frequency

  # Define scales for EMG signal analysis
  min_frequency = 10  # Minimum frequency of interest (e.g., muscle activity)

  # Generate logarithmically spaced scales
  wavelet = "morl"
  cwt_data = np.ndarray(shape=(data.shape[0], data.shape[1], num_scales, data.shape[2]))
  frequencies = np.flip((np.logspace(np.log10(1), np.log10(nyquist_frequency / min_frequency), num_scales) * min_frequency) / sampling_rate)
  scale_list = pywt.frequency2scale(wavelet, frequencies)

  for idx, i in enumerate(data):
  # plot_fft("fft",i[0], i[1])
    for idj, j in enumerate(i):
      coeffs, freqs = pywt.cwt(j, scale_list, wavelet, sampling_period=1/sampling_rate)
      cwt_data[idx, idj, :, :] = coeffs
    # graph_gram(f' cwt ', coeffs, freqs)

  return cwt_data

def calculate_rms(data):
  return np.round(np.sqrt(np.power(data,2).mean(axis=2))).astype('int')
