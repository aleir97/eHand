'''
  - Python module for pattern classification at EMG samples via neural networks

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
sys.path.insert(1,'/Users/aleir97/Documents/ehand/python')
import os
from tinygrad import nn
from tinygrad.nn import optim
from tinygrad.tensor import Tensor
from tinygrad.nn.state import get_parameters
from tinygrad.nn.state import safe_save, safe_load, get_state_dict, load_state_dict
from tinygrad.dtype import dtypes

import numpy as np
from sklearn.model_selection import KFold
from mlxtend.plotting import plot_decision_regions
from utils.data_utils import get_data, calculate_rms
import matplotlib.pyplot as plt

class rms_nnet:
	def __init__(self):
		#This applies Linear transformation to input data.
		self.fc1 = nn.Linear(2, 4)

	def forward(self, x):
		#Output of the first layer
		return self.fc1(x)

	#This function takes an input and predicts the class, (Resting, Flex, Ext, Fist)
	def predict(self, x):
		x = Tensor(x, dtype=dtypes.float16)
		# Forward model with the input
		pred = self.forward(x).softmax()

		return pred.argmax(1).numpy().astype(int)

	def reset_weights(self):
		self.fc1.reset_parameters()

def train_epoch(model, data, targets, optimizer):
	y_pred = model.forward(data)
	# Compute Cross entropy loss
	loss = y_pred.sparse_categorical_crossentropy(targets)
	# Clear the previous gradients
	optimizer.zero_grad()
	# Compute gradients
	loss.backward()
	# Adjust weights
	optimizer.step()
	return loss.numpy()

def valid_epoch(model, data, targets):
	# Predict the output for Given input
	y_pred = model.forward(data)
	# Compute Cross entropy loss
	loss = y_pred.sparse_categorical_crossentropy(targets)
	return loss.numpy()

def train_valid_nnet(raw_data, raw_targets, safe=False):
	# Build the model
	model = rms_nnet()

	# Define the optimizer
	optimizer = optim.Adam(get_parameters(model), lr=0.05)

	# Number of epochs
	epochs = 1000

	splits = KFold(n_splits=5, random_state=17, shuffle=True)

	for fold, (train_idx, val_idx) in enumerate(splits.split(np.arange(len(raw_data)))):
		# Loss calculation
		training_loss, valid_loss = 0.0,  0.0

		for w in range(epochs):
			training_loss += train_epoch(model, Tensor(raw_data[train_idx],dtype=dtypes.float16), Tensor(raw_targets[train_idx],dtype=dtypes.float16), optimizer)
			valid_loss += valid_epoch(model, Tensor(raw_data[val_idx],dtype=dtypes.float16), Tensor(raw_targets[val_idx],dtype=dtypes.float16))

			if w == (epochs-1):
				print("FOLD: ", fold, " Epoch: ", w, "Training loss: ", training_loss/(len(train_idx)*epochs), "Validation Loss: ", valid_loss/(len(val_idx)*epochs))

		if not safe:
			# Reset model parameters between folds to make an entire validation
			model.reset_weights()

	if safe:
		# wrapper = ModelWrapper(model)
		model.predict(raw_data.astype(int))

		plot_decision_regions(raw_data.astype(int), raw_targets.astype(int), model, legend=4)
		plt.show()

		if ( input('Are u sure u wanna save? YES|NO ') == 'YES' ):
			safe_save(get_state_dict(model), "model.safetensors")
		else:
			exit()

def main():
	data, targets = get_data(os.scandir('/Users/aleir97/Documents/ehand/emg_data/26-2023-05'))
	data = calculate_rms(data)
	train_valid_nnet(data, targets, True)

	# model = torch.load("D:\PROYECTO_MANO_FPGA\GIT\python\models\ehand_nnet.sav")
	# classification(256, model)

if __name__ == "__main__":
	main()


