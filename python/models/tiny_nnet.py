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

from tinygrad import nn
from tinygrad.nn import optim
from tinygrad.tensor import Tensor

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from mlxtend.plotting import plot_decision_regions

import os
os.environ["GPU"] = "1"
from data_utils import *

def sparse_categorical_crossentropy(out, Y):
  num_classes = out.shape[-1]
  YY = Y.flatten()
  y = np.zeros((YY.shape[0], num_classes), np.float32)
  # correct loss for NLL, torch NLL loss returns one per row
  y[range(y.shape[0]),int(YY.numpy())] = -1.0*num_classes
  y = y.reshape(list(Y.shape)+[num_classes])
  y = Tensor(y)
  return out.mul(y).mean()

# class ModelWrapper():
# 	def __init__(self, model):
# 		self.model = model
        
# 	def predict(self, x):
# 		features = torch.tensor(x, dtype= torch.float)
# 		_, predicted_labels = torch.max(self.model(features), 1)

# 		return predicted_labels.numpy()

class rms_nnet:
	def __init__(self):
		#This applies Linear transformation to input data. 
		self.fc1 = nn.Linear(2, 4)

	def forward(self, x):
		#Output of the first layer
		return self.fc1(x).log_softmax()

	#This function takes an input and predicts the class, (Resting, Flex, Ext, Fist)        
	def predict(self, x):
		x = Tensor(x)	
		# Forward model with the input
		pred = self.forward(x)
		
		return [pred.max().indices.item()]

	def reset_weights(self):
		self.fc1.reset_parameters()	

def train_epoch(model, data, targets, train_idx, criterion, optimizer):
	training_loss = 0.0 

	for i in range(len(train_idx)):
		#Predict the output for Given input
		# TODO: fix indexing bug
		idx = int(train_idx[i])
		y_pred = model.forward(data[idx])

		#Compute Cross entropy loss
		loss = criterion(y_pred, targets[idx])

		#Clear the previous gradients
		optimizer.zero_grad()

		#Compute gradients
		loss.backward()

		#Adjust weights
		optimizer.step()

		training_loss += loss.numpy()[0]

	return training_loss 

def valid_epoch(model, data, targets, val_idx, criterion):
	valid_loss = 0.0 

	for i in range(len(val_idx)):
		#Predict the output for Given input
		idx = int(val_idx[i])
		y_pred = model.forward(data[idx])

		#Compute Cross entropy loss
		loss = criterion(y_pred, targets[idx])

		valid_loss += loss.numpy()[0]

	return valid_loss

def train_valid_nnet(raw_data, raw_targets, safe=False):
	data    = Tensor(raw_data)
	targets = Tensor(raw_targets)
	
	# Build the model
	model = rms_nnet()

	# Define loss criterion
	criterion = sparse_categorical_crossentropy

	# Define the optimizer
	params = optim.get_parameters(model)
	[x.gpu_() for x in params]

	optimizer = optim.Adam(optim.get_parameters(model), lr=0.05)

	# Number of epochs
	epochs = 100
	
	splits = KFold(n_splits=5, random_state=17, shuffle=True)
	
	for fold, (train_idx, val_idx) in enumerate(splits.split(np.arange(len(raw_data)))):
		# Loss calculation
		training_loss, valid_loss = 0.0,  0.0

		for w in range(epochs):
			training_loss += train_epoch(model, data, targets, train_idx, criterion, optimizer)	
			valid_loss += valid_epoch(model, data, targets, val_idx, criterion)
		
			if w == (epochs-1):
				print("FOLD: ", fold, " Epoch: ", w, "Training loss: ", training_loss/(len(train_idx)*epochs), "Validation Loss: ", valid_loss/(len(val_idx)*epochs))
		
		if not safe:
			# Reset model parameters between folds to make an entire validation		 
			model.reset_weights()
	
	# if safe:
		# wrapper = ModelWrapper(model)
		# plot_decision_regions(raw_data, raw_targets, wrapper, legend=4)
		# plt.show()

		# if ( input('Are u sure u wanna save? YES|NO ') == 'YES' ):
		# 	torch.save(model,'ehand_nnet.sav')    
		# else:
		# 	exit()

def main():
	used_samples = 256
	data, targets = get_data(used_samples)
	train_valid_nnet(data, targets, True)
	
	# model = torch.load("D:\PROYECTO_MANO_FPGA\GIT\python\models\ehand_nnet.sav")
	# classification(256, model)

if __name__ == "__main__":
	main()


