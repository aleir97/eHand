import numpy as np
import pandas as pd
import os 
import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn import svm 
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import serial
import time
import pickle

dataSet_path = r'D:\PROYECTO_MANO_FPGA\GIT\PY\eHand\Arduino\\'

def generate_dataset(samples):
    dataSet_dire = dataSet_path+ 'dataset'
    ind =-1
    for entry in os.scandir(dataSet_dire):
        if (entry.is_file()):
            ind += 1
            
            signal = pd.read_csv(entry.path)
            
            ch1, ch2 = signal["CH1"].to_numpy(), signal["CH2"].to_numpy()    
            ch1, ch2  = ch1[1:samples+1], ch2[1:samples+1] 
        
            ch1rms, ch2rms = int (np.round(np.sqrt(np.mean(ch1**2)))), int (np.round(np.sqrt(np.mean(ch2**2))))         
            
            #print("DATA FROM FILE: "+ entry.name)
            #print("RMS CH2 VAL:"+ str(ch1rms))
            #print("RMS CH2 VAL:"+ str(ch2rms))

            if "rest" in entry.name:
                mvmnt = 0
            elif 'flex'  in entry.name:
                mvmnt = 1 
            elif 'ext' in entry.name:
                mvmnt = 2
            elif 'fist' in entry.name:
                mvmnt = 3

            data = {'CH1': ch1rms,
            'CH2': ch2rms,
            'class': mvmnt    
            }

            if (ind == 0):
                 df = pd.DataFrame(data, columns= ['CH1', 'CH2', 'class'], index = [ind])

            else:
                df2 = pd.DataFrame(data, columns= ['CH1', 'CH2', 'class'], index = [0]) 
                df = df.append(df2, ignore_index= True)

    path = r'D:\PROYECTO_MANO_FPGA\GIT\PY\eHand\\'+ 'dataSet'+ '.csv' 
    df.to_csv(path, index = False, header=True)            
   
def svm_classifier():
    data_path = dataSet_path+ 'dataSet.csv'
    dataSet = pd.read_csv(data_path)

    data = np.dstack((dataSet["CH1"].to_numpy(), dataSet["CH2"].to_numpy()))
    data = data.reshape(data.shape[1:])

    targets = dataSet['class'].to_numpy()

    accuracy_lin, accuracy_poly, accuracy_rbf, accuracy_sig = 0, 0, 0 ,0   

    # Mean calculations for score
    for i in range(1,11):
        X_train, X_test, y_train, y_test= train_test_split(data, targets, test_size=0.3, random_state=109)

        linear = svm.SVC(kernel='linear', C=1, decision_function_shape='ovo').fit(X_train, y_train)
        rbf = svm.SVC(kernel='rbf', gamma=1, C=1, decision_function_shape='ovo').fit(X_train, y_train)
        poly = svm.SVC(kernel='poly', degree=3, C=1, decision_function_shape='ovo').fit(X_train, y_train)
        sig = svm.SVC(kernel='sigmoid', C=1, decision_function_shape='ovo').fit(X_train, y_train)

        # Retrieve the accuracy and print it for all 4 kernel functions 
        accuracy_lin += linear.score(X_test, y_test)
        accuracy_poly += poly.score(X_test, y_test)
        accuracy_rbf += rbf.score(X_test, y_test)
        accuracy_sig += sig.score(X_test, y_test)

    accuracy_lin, accuracy_poly, accuracy_rbf, accuracy_sig = accuracy_lin/10, accuracy_poly/10, accuracy_rbf/10, accuracy_sig/10 
    print("\n\n****************************************")
    print("RESULTS FROM SVM CLASSIFICATION")
    print("Accuracy Linear Kernel:", accuracy_lin)
    print("Accuracy Polynomial Kernel:", accuracy_poly)
    print("Accuracy Radial Basis Kernel:", accuracy_rbf)
    print("Accuracy Sigmoid Kernel:", accuracy_sig)

    # k - Fold validation of linear model
    X=  dataSet.iloc[:,:-1]
    y=  dataSet.iloc[:,-1]
    
    # prepare the cross-validation procedure
    cv = KFold(n_splits=3, random_state=1, shuffle=True)
    
    # evaluate model
    scores = cross_val_score(linear, X, y, scoring='accuracy', cv=cv, n_jobs=-1)
    
    # report performance
    print('\n k - Fold Accuracy of linear model: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))

    # Print model response
    # Stepsize in the mesh, it alters the accuracy of the plotprint
    # to better understand it, just play with the value, change it and print it
    h = .1
    
    # Create the mesh
    x_min, x_max = data[:, 0].min() - 1, data[:, 0].max() + 1
    y_min, y_max = data[:, 1].min() - 1, data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),np.arange(y_min, y_max, h))
    
    #titles = ['Linear kernel','Polynomial kernel','RBF kernel','Sigmoid kernel']
    titles = ['Linear kernel', 'Polynomial kernel']
    
    #for i, clf in enumerate((linear, poly, rbf, sig)):
    for i, clf in enumerate((linear, poly)):    
        plt.subplot(2, 2, i + 1)
        plt.subplots_adjust(wspace=0.4, hspace=0.4)    
    
        # Put the result into a color plot     
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])    
        Z = Z.reshape(xx.shape)
        
        plt.contourf(xx, yy, Z, cmap=plt.cm.PuBuGn, alpha=0.7)    # Plot also the training points
        plt.scatter(data[:, 0], data[:, 1], c=targets, cmap=plt.cm.PuBuGn, edgecolors='grey')    
        plt.xlabel('Sepal length')
        plt.ylabel('Sepal width')
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.xticks(())
        plt.yticks(())
        plt.title(titles[i])    
        
    plt.show()

    filename = './ehand.sav'
    pickle.dump(linear, open(filename, 'wb'))

    
    #if ((accuracy_lin >= accuracy_poly) and (accuracy_lin >= accuracy_rbf) and (accuracy_lin >= accuracy_sig)):
    #return linear

    #elif ((accuracy_poly >= accuracy_lin) and (accuracy_poly >= accuracy_rbf) and (accuracy_poly >= accuracy_sig)):
    #    return poly

def classification(used_samples):
    # Conexion con el arduino, lectura de used samples 
    # hacer una "libreria que me devuelva resultados"
    # sacar RMS y usar valores para la clasificacion
    # mapear tecla -> modelo 3D o juego
    
    f = open("D:\\PROYECTO_MANO_FPGA\\GIT\\PY\\3D\\com.txt", "w")
    state = ''

    filename = './ehand.sav'
    svm = pickle.load(open(filename, 'rb'))

    # Serial port connection
    port = serial.Serial('COM3', baudrate=115200, timeout=0.5) # Establish connection with arduino
    port.setDTR(False)
    time.sleep(1)
    port.flushInput()
    port.setDTR(True)
    
    A1 = []
    A2 = []
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
                    #print('MEASURE A1:', port.readline().decode('ascii'))
                    #print('MEASURE A2:', port.readline().decode('ascii'))
                    A1.append(port.readline().decode('ascii'))
                    A2.append(port.readline().decode('ascii'))
                    
                A1=np.fromiter(map(int, A1), dtype=int) 
                A2=np.fromiter(map(int, A2), dtype=int)

                ch1rms, ch2rms = int (np.round(np.sqrt(np.mean(A1**2)))), int (np.round(np.sqrt(np.mean(A2**2))))    
                
                #print("RMS CH1:%d, CH2:%d\n" % (ch1rms, ch2rms))

                hand_mvn = svm.predict(np.reshape([ch1rms, ch2rms], (-1, 2)))
                print(hand_mvn)
                # AÑADIR VARIABLE ESTADO PARA NO ANDAR ESCRIBIENDO LO MISMO TODO EL RATO
                if hand_mvn[0] == 0:
                    state = 'REP'
                    f.seek(0)
                    f.write('REP\n')
                    f.truncate()

                elif hand_mvn[0] == 1:
                    state = 'FLEX'
                    f.seek(0)
                    f.write('FLEX\n')
                    f.truncate()
                     
                elif hand_mvn[0] == 2:
                    state = 'EXT'
                    f.seek(0)
                    f.write('EXT\n')
                    f.truncate()

                time.sleep(0.10)
        else:
            port.write(bytes(b'stop'))  

    return 0

def main():
    used_samples = 256
    generate_dataset(used_samples)
    
    #svm_classifier()
    
    classification(used_samples)

if __name__ == "__main__":
    main()