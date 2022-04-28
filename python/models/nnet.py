import torch
from torch import nn
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import torch.nn.functional as F
from sklearn.model_selection import KFold
import serial
import time

import sys
sys.path.insert(1, '../utils')
from data_utils import generate_dataset

dataSet_path = r'D:\PROYECTO_MANO_FPGA\GIT\python\models'

class rms_nnet(nn.Module):
	def __init__(self):
		super(rms_nnet, self).__init__()
		#Our network consists of 4 layers. 1 input, 1 hidden and 1 output layer
		#This applies Linear transformation to input data. 
		self.fc1 = nn.Linear(2, 10)
        
		#This applies linear transformation to produce output data
		self.fc2 = nn.Linear(10, 4)
		
		#self.fc3 = nn.Linear(50, 4)


	def forward(self, x):
		#Output of the first layer
		#Activation function is Relu. Feel free to experiment with this
		x = self.fc1(x)
		x = F.relu(x)

 		# To second layer
		x = self.fc2(x)
		#x = F.relu(x)

		#This produces output
		#x = self.fc3(x)

		return x


	#This function takes an input and predicts the class, (Resting, Flex, Ext, Fist)        
	def predict(self, x):
		#Apply softmax to output. 
		pred = F.softmax(self.forward(x), dim=-1)
		ans = []

		#Pick the class with maximum weight
		i = 0 
		aux = 0 
		for t in pred:	
			out = int (np.round((t.item()*100) , 2))
			#print('Value for neuron',i, 'is: ',out,'%')

			if (out > aux):
				res = i
				aux = out

			i +=1
					
		return res

	def reset_weights(self):
		self.fc1.reset_parameters()	
		self.fc2.reset_parameters()	


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


def train_valid_nnet(safe):
	data_path = dataSet_path+ '\\dataSet.csv'
	dataSet = pd.read_csv(data_path)

	data = np.dstack((dataSet["CH1"].to_numpy(), dataSet["CH2"].to_numpy()))
	data = data.reshape(data.shape[1:])
	targets = dataSet['class'].to_numpy()

	data = torch.tensor(data, dtype= torch.float)
	targets = torch.tensor(targets, dtype= torch.long)
	
	# Build the model
	model = rms_nnet()

	# Define loss criterion
	criterion = nn.CrossEntropyLoss()
	# Define the optimizer
	optimizer = torch.optim.Adam(model.parameters(), lr=0.02)

	# Number of epochs
	epochs = 15 
	
	# Loss calculation
	training_loss, valid_loss = 0.0,  0.0

	splits = KFold(n_splits=3, random_state=42, shuffle=True)
	
	for fold, (train_idx, val_idx) in enumerate(splits.split(np.arange(len(data)))):
		for w in range(epochs):
			training_loss = train_epoch(model, data, targets, train_idx, criterion, optimizer)	
			valid_loss = valid_epoch(model, data, targets, val_idx, criterion, optimizer)
		
			if w == (epochs-1):
				print("FOLD: ", fold, " Epoch: ", w, "Training loss: ", training_loss/(len(train_idx)), "Validation Loss: ", valid_loss/(len(val_idx)))

		if not safe:
			# Reset model parameters between folds to make an entire validation		 
			model.reset_weights()

	if safe:
		print('Are u sure u wanna save? YES|NO ')
		if ( input() == 'YES' ):
			torch.save(model,'ehand_nnet.sav')    
		else:
			exit()


def classification(used_samples, model):
    # TODO: Conexion con el arduino, lectura de used samples 
    # hacer una "libreria que me devuelva resultados" y otra para inyectarselos algo concurrente (?)
    
    f = open("D:\\PROYECTO_MANO_FPGA\\GIT\\python\\3D\\com.txt", "w")
    state = ''

    # Serial port connection
    port = serial.Serial('COM3', baudrate=115200, timeout=0.5) # Establish connection with arduino
    port.setDTR(False)
    time.sleep(1)
    port.flushInput()
    port.setDTR(True)
    
    A1 = []
    A2 = []
    hits = 0
    last_predict = 0
    input('THE MODEL IS READY TO CLASSIFY, PLS PRESS ENTER TO CONNECT TO THE ARDUINO AND BEGIN')
    while True:
        # Send the signal sync to arduino
        port.write(bytes(b'ini'))
        
        # Receiving signal sync from arduino 
        for i in range(10):
            line = port.readline().decode('ascii')
            if line == 'ini\r\n':
                break
        
        if line == 'ini\r\n':
            while True:
                A1 = []
                A2 = []
                for i in range(used_samples):
                    A1.append(port.readline().decode('ascii'))
                    A2.append(port.readline().decode('ascii'))
                    
                A1=np.fromiter(map(int, A1), dtype=int) 
                A2=np.fromiter(map(int, A2), dtype=int)

                ch1rms, ch2rms = int (np.round(np.sqrt(np.mean(A1**2)))), int (np.round(np.sqrt(np.mean(A2**2))))    
                
                #print("RMS CH1:%d, CH2:%d\n" % (ch1rms, ch2rms))

                data = torch.tensor([ch1rms, ch2rms], dtype= torch.float)
                hand_mvn = model.predict(data)
                
                if last_predict == hand_mvn:
                    hits += 1
                else:
                    hits = 0

                if (hits == 3 and hand_mvn == 0 and state != 'REP'):
                    print(hand_mvn)
					#keyboard.release("right")
                    #keyboard.release("left")
                    #keyboard.release("z")
                    
                    state = 'REP'
                    f.seek(0)
                    f.write('REP\n')
                    f.truncate()

                elif (hits == 3 and hand_mvn == 1 and state != 'FLEX'):
                    print(hand_mvn)
                    #keyboard.press("right")
                    state = 'FLEX'
                    f.seek(0)
                    f.write('FLEX\n')
                    f.truncate()
                     
                elif (hits == 3 and hand_mvn == 2  and state != 'EXT') :
                    print(hand_mvn)
                    #keyboard.press("left")
                    state = 'EXT'
                    f.seek(0)
                    f.write('EXT\n')
                    f.truncate()

                elif (hits == 3 and hand_mvn == 3  and state != 'FIST') :
                    print(hand_mvn)
                    #keyboard.press("z")
                    state = 'FIST'
                    f.seek(0)
                    f.write('FIST\n')
                    f.truncate()

                last_predict = hand_mvn 
				#time.sleep(0.10)
        else:
            port.write(bytes(b'stop'))  


    return 0




def main():
	#train_valid_nnet(True)

	model = torch.load("D:\PROYECTO_MANO_FPGA\GIT\python\models\ehand_nnet.sav")
	#classification(256, model)


if __name__ == "__main__":
	main()


