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


import torch
from torch import nn
from torch.autograd import Variable
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import torch.nn.functional as F
from sklearn.model_selection import KFold
from mlxtend.plotting import plot_decision_regions

import sys
sys.path.insert(1, '../utils')
from data_utils import *

dataSet_path = r'D:\PROYECTO_MANO_FPGA\GIT\python\models'
	
class ModelWrapper():
	def __init__(self, model):
		self.model = model
        
	def predict(self, x):
		features = torch.tensor(x, dtype= torch.float)
		_, predicted_labels = torch.max(self.model(features), 1)

		return predicted_labels.numpy()

class rms_nnet(nn.Module):
	def __init__(self):
		super(rms_nnet, self).__init__()
		
		#This applies Linear transformation to input data. 
		self.fc1 = nn.Linear(2, 4)

	def forward(self, x):
		#Output of the first layer
		x = self.fc1(x)

		return x

	#This function takes an input and predicts the class, (Resting, Flex, Ext, Fist)        
	def predict(self, x):
		x = torch.tensor(x, dtype= torch.float)	
		#Apply softmax to output. 
		pred = F.softmax(self.forward(x), dim=-1)
		
		return [torch.max(pred, -1).indices.item()]

	def reset_weights(self):
		self.fc1.reset_parameters()	

def train_epoch(model, data, targets, train_idx, criterion, optimizer):
	training_loss = 0.0 

	for i in range(len(train_idx)):
		#Predict the output for Given input
		y_pred = model.forward(data[train_idx[i]])

		#Compute Cross entropy loss
		loss = criterion(y_pred, targets[train_idx[i]])

		#Clear the previous gradients
		optimizer.zero_grad()

		#Compute gradients
		loss.backward()

		#Adjust weights
		optimizer.step()

		training_loss += loss.item()	

	return training_loss 

def valid_epoch(model, data, targets, val_idx, criterion, optimizer):
	valid_loss = 0.0 

	for i in range(len(val_idx)):
		#Predict the output for Given input
		y_pred = model.forward(data[val_idx[i]])

		#Compute Cross entropy loss
		loss = criterion(y_pred, targets[val_idx[i]])

		valid_loss += loss.item()

	return valid_loss

def train_valid_nnet(raw_data, raw_targets, safe=False):
	data = torch.tensor(raw_data, dtype= torch.float)
	targets = torch.tensor(raw_targets, dtype= torch.long)
	
	# Build the model
	model = rms_nnet()

	# Define loss criterion
	criterion = nn.CrossEntropyLoss()
	# Define the optimizer
	optimizer = torch.optim.Adam(model.parameters(), lr=0.05)

	# Number of epochs
	epochs = 100
	
	splits = KFold(n_splits=5, random_state=17, shuffle=True)
	
	for fold, (train_idx, val_idx) in enumerate(splits.split(np.arange(len(data)))):
		# Loss calculation
		training_loss, valid_loss = 0.0,  0.0

		for w in range(epochs):
			training_loss += train_epoch(model, data, targets, train_idx, criterion, optimizer)	
			valid_loss += valid_epoch(model, data, targets, val_idx, criterion, optimizer)
		
			if w == (epochs-1):
				print("FOLD: ", fold, " Epoch: ", w, "Training loss: ", training_loss/(len(train_idx)*epochs), "Validation Loss: ", valid_loss/(len(val_idx)*epochs))
		
		if not safe:
			# Reset model parameters between folds to make an entire validation		 
			model.reset_weights()
	
	if safe:
		wrapper = ModelWrapper(model)
		plot_decision_regions(raw_data, raw_targets, wrapper, legend=4)
		plt.show()

		if ( input('Are u sure u wanna save? YES|NO ') == 'YES' ):
			torch.save(model,'ehand_nnet.sav')    
		else:
			exit()

def main():
	#data, targets = get_data(used_samples)
	#data = torch.tensor(data, dtype= torch.float)
	#train_valid_nnet(data, targets, True)
	
	model = torch.load("D:\PROYECTO_MANO_FPGA\GIT\python\models\ehand_nnet.sav")
	classification(256, model)

if __name__ == "__main__":
	main()


