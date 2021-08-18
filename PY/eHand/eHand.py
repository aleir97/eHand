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

dataSet_path = r'D:\PROYECTO_MANO_FPGA\GIT\PY\eHand\\'

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
    
    titles = ['Linear kernel','Polynomial kernel','RBF kernel','Sigmoid kernel']
    
    for i, clf in enumerate((linear, poly, rbf, sig)):
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

    if ((accuracy_lin >= accuracy_poly) and (accuracy_lin >= accuracy_rbf) and (accuracy_lin >= accuracy_sig)):
        return linear

    elif ((accuracy_poly >= accuracy_lin) and (accuracy_poly >= accuracy_rbf) and (accuracy_poly >= accuracy_sig)):
        return poly

def classification(svm, used_samples):
    # Conexion con el arduino, lectura de used samples 
    # hacer una "libreria que me devuelva resultados"
    # sacar RMS y usar valores para la clasificacion
    # mapear tecla -> modelo 3D o juego
    return 0

def main():
    used_samples = 256
    generate_dataset(used_samples)
    
    classification(svm_classifier(), used_samples)

if __name__ == "__main__":
    main()