import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm 
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import serial
import pickle
import keyboard

import sys
sys.path.insert(1, '../utils')
from data_utils import generate_dataset

           
def train_svm():
    data_path = dataSet_path+ '\\dataSet.csv'
    dataSet = pd.read_csv(data_path)

    data = np.dstack((dataSet["CH1"].to_numpy(), dataSet["CH2"].to_numpy()))
    data = data.reshape(data.shape[1:])

    targets = dataSet['class'].to_numpy()

    #accuracy_lin, accuracy_poly, accuracy_rbf, accuracy_sig = 0, 0, 0 ,0   

    # Mean calculations for score
    #for i in range(1,11):
    
    #linear = svm.SVC(kernel='linear', C=1, decision_function_shape='ovo')
    #rbf = svm.SVC(kernel='rbf', gamma=1, C=1, decision_function_shape='ovo')
    #poly = svm.SVC(kernel='poly', degree=3, C=1, decision_function_shape='ovo')
    #sig = svm.SVC(kernel='sigmoid', C=1, decision_function_shape='ovo')

    # Retrieve the accuracy and print it for all 4 kernel functions 
    #accuracy_lin += linear.score(X_test, y_test)
    #accuracy_poly += poly.score(X_test, y_test)
    #accuracy_rbf += rbf.score(X_test, y_test)
    #accuracy_sig += sig.score(X_test, y_test)

    #accuracy_lin, accuracy_poly, accuracy_rbf, accuracy_sig = accuracy_lin/10, accuracy_poly/10, accuracy_rbf/10, accuracy_sig/10 
    #print("\n\n****************************************")
    #print("RESULTS FROM SVM CLASSIFICATION")
    #print("Accuracy Linear Kernel:", accuracy_lin)
    #print("Accuracy Polynomial Kernel:", accuracy_poly)
    #print("Accuracy Radial Basis Kernel:", accuracy_rbf)
    #print("Accuracy Sigmoid Kernel:", accuracy_sig)

    linear = svm.SVC(kernel='linear', C=1, decision_function_shape='ovo')
    rbf = svm.SVC(kernel='rbf', gamma=1, C=1, decision_function_shape='ovo')
    poly = svm.SVC(kernel='poly', degree=3, C=1, decision_function_shape='ovo')
    sig = svm.SVC(kernel='sigmoid', C=1, decision_function_shape='ovo')

    # k - Fold validation of linear model
    X=  dataSet.iloc[:,:-1]
    y=  dataSet.iloc[:,-1]
    
    # prepare the cross-validation procedure
    cv = KFold(n_splits=3, random_state=1, shuffle=True)
    
    # evaluate model
    scores = cross_val_score(linear, X, y, scoring='accuracy', cv=cv, n_jobs=-1)
    
    # report performance
    print('\n k - Fold Accuracy of linear model: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))

    scores = cross_val_score(poly, X, y, scoring='accuracy', cv=cv, n_jobs=-1)
    
    # report performance
    print('\n k - Fold Accuracy of poly model: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))

    scores = cross_val_score(rbf, X, y, scoring='accuracy', cv=cv, n_jobs=-1)
    
    # report performance
    print('\n k - Fold Accuracy of rbf model: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))

    scores = cross_val_score(sig, X, y, scoring='accuracy', cv=cv, n_jobs=-1)
    
    # report performance
    print('\n k - Fold Accuracy of sig model: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))


    #X_train, X_test, y_train, y_test= train_test_split(data, targets, test_size=0.3, random_state=109)
    
    linear = svm.SVC(kernel='linear', C=1, decision_function_shape='ovo').fit(X, y)
    rbf = svm.SVC(kernel='rbf', gamma=1, C=1, decision_function_shape='ovo').fit(X, y)
    poly = svm.SVC(kernel='poly', degree=3, C=1, decision_function_shape='ovo').fit(X, y)
    sig = svm.SVC(kernel='sigmoid', C=1, decision_function_shape='ovo').fit(X, y)

    # Print model response
    # Stepsize in the mesh, it alters the accuracy of the plotprint
    # to better understand it, just play with the value, change it and print it
    h = .1
    
    # Create the mesh
    x_min, x_max = data[:, 0].min() - 1, data[:, 0].max() + 1
    y_min, y_max = data[:, 1].min() - 1, data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),np.arange(y_min, y_max, h))
    
    titles = ['Linear kernel','Polynomial kernel','RBF kernel','Sigmoid kernel']
    #titles = ['Linear kernel', 'Polynomial kernel']
    
    for i, clf in enumerate((linear, poly, rbf, sig)):
    #for i, clf in enumerate((linear, poly)):    
        plt.subplot(2, 2, i + 1)
        plt.subplots_adjust(wspace=0.4, hspace=0.4)    
    
        # Put the result into a color plot     
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])    
        Z = Z.reshape(xx.shape)
        
        plt.contourf(xx, yy, Z, cmap=plt.cm.PuBuGn, alpha=0.7)    # Plot also the training points
        plt.scatter(data[:, 0], data[:, 1], c=targets, cmap=plt.cm.PuBuGn, edgecolors='grey')    
        plt.xlabel('RMS on Ch1')
        plt.ylabel('RMS on Ch2')
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.xticks(())
        plt.yticks(())
        plt.title(titles[i])    
        
    plt.show()

    filename = './ehand_svm.sav'
    pickle.dump(linear, open(filename, 'wb'))


def classification(used_samples):
    # Conexion con el arduino, lectura de used samples 
    # hacer una "libreria que me devuelva resultados"
    # sacar RMS y usar valores para la clasificacion
    # mapear tecla -> modelo 3D o juego
    
    f = open("D:\\PROYECTO_MANO_FPGA\\GIT\\python\\3D\\com.txt", "w")
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
                    A1.append(port.readline().decode('ascii'))
                    A2.append(port.readline().decode('ascii'))
                    
                A1=np.fromiter(map(int, A1), dtype=int) 
                A2=np.fromiter(map(int, A2), dtype=int)

                ch1rms, ch2rms = int (np.round(np.sqrt(np.mean(A1**2)))), int (np.round(np.sqrt(np.mean(A2**2))))    
                
                #print("RMS CH1:%d, CH2:%d\n" % (ch1rms, ch2rms))

                hand_mvn = svm.predict(np.reshape([ch1rms, ch2rms], (-1, 2)))
                print(hand_mvn)
              
                if (hand_mvn[0] == 0 and state != 'REP'):
                    
                    keyboard.release("right")
                    keyboard.release("left")
                    keyboard.release("z")
                    
                    state = 'REP'
                    #f.seek(0)
                    #f.write('REP\n')
                    #f.truncate()

                elif (hand_mvn[0] == 1 and state != 'FLEX'):
                    keyboard.press("right")
                    state = 'FLEX'
                    #f.seek(0)
                    #f.write('FLEX\n')
                    #f.truncate()
                     
                elif (hand_mvn[0] == 2  and state != 'EXT') :
                    keyboard.press("left")
                    state = 'EXT'
                    #f.seek(0)
                    #f.write('EXT\n')
                    #f.truncate()

                elif (hand_mvn[0] == 3  and state != 'FIST') :
                    keyboard.press("z")
                    state = 'FIST'
                    #f.seek(0)
                    #f.write('FIST\n')
                    #f.truncate()

                time.sleep(0.10)
        else:
            port.write(bytes(b'stop'))  

    return 0

def main():
    used_samples = 250
    generate_dataset(used_samples)
   
    #train_svm()
    
    #classification(used_samples)

if __name__ == "__main__":
    main()
