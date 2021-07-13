import numpy as np
import pandas as pd
import os 
import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn import svm 
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

def generate_dataset(samples):
    dire = r'D:\PROYECTO_MANO_FPGA\GIT\PY\eHand\dataset'
    ind =-1
    for entry in os.scandir(dire):
        if (entry.is_file()):
            ind += 1
            print("DATA FROM FILE: "+ entry.name)
            
            signal = pd.read_csv(entry.path)
            ch1 = signal["CH1"].to_numpy()
            ch2 = signal["CH2"].to_numpy()    

            ch1 = ch1[1:samples+1]
            ch2 = ch2[1:samples+1]
            #print("USING N SAMPLES = "+ str(len(ch1)))

            ch1rms = int (np.round(np.sqrt(np.mean(ch1**2))))         
            ch2rms = int (np.round(np.sqrt(np.mean(ch2**2))))
            
            print("RMS CH2 VAL:"+ str(ch1rms))
            print("RMS CH2 VAL:"+ str(ch2rms))

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

    path = r'D:\PROYECTO_MANO_FPGA\GIT\PY\\'+ 'dataSet'+ '.csv' 
    df.to_csv(path, index = False, header=True)            
   
def svm_classifier():
    data_path = r'D:\PROYECTO_MANO_FPGA\GIT\PY\dataSet.csv'
    dataSet = pd.read_csv(data_path)

    data = np.dstack((dataSet["CH1"].to_numpy(), dataSet["CH2"].to_numpy()))
    data = data.reshape(data.shape[1:])

    targets = dataSet['class'].to_numpy()

    X_train, X_test, y_train, y_test= train_test_split(data, targets, test_size=0.3,random_state=109)

    linear = svm.SVC(kernel='linear', C=1, decision_function_shape='ovo').fit(X_train, y_train)
    rbf = svm.SVC(kernel='rbf', gamma=1, C=1, decision_function_shape='ovo').fit(X_train, y_train)
    poly = svm.SVC(kernel='poly', degree=3, C=1, decision_function_shape='ovo').fit(X_train, y_train)
    sig = svm.SVC(kernel='sigmoid', C=1, decision_function_shape='ovo').fit(X_train, y_train)

    # retrieve the accuracy and print it for all 4 kernel functions
    accuracy_lin = linear.score(X_test, y_test)
    accuracy_poly = poly.score(X_test, y_test)
    accuracy_rbf = rbf.score(X_test, y_test)
    accuracy_sig = sig.score(X_test, y_test)

    print("\n\n****************************************")
    print("RESULTS FROM SVM CLASSIFICATION")
    print("Accuracy Linear Kernel:", accuracy_lin)
    print("Accuracy Polynomial Kernel:", accuracy_poly)
    print("Accuracy Radial Basis Kernel:", accuracy_rbf)
    print("Accuracy Sigmoid Kernel:", accuracy_sig)
    
    #stepsize in the mesh, it alters the accuracy of the plotprint
    to better understand it, just play with the value, change it and print it
    h = .01
        create the mesh
    x_min, x_max = data[:, 0].min() - 1, data[:, 0].max() + 1
    y_min, y_max = data[:, 1].min() - 1, data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),np.arange(y_min, y_max, h))# create the title that will be shown on the plot
    titles = ['Linear kernel','RBF kernel','Polynomial kernel','Sigmoid kernel']
    
    for i, clf in enumerate((linear, rbf)):
    #for i, clf in enumerate((linear, rbf, poly, sig)):
        #defines how many plots: 2 rows, 2columns=> leading to 4 plots
        plt.subplot(2, 2, i + 1) #i+1 is the index
    
        #space between plots
        plt.subplots_adjust(wspace=0.4, hspace=0.4)    
    
        # Put the result into a color plot     
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])    
        Z = Z.reshape(xx.shape)
        
        plt.contourf(xx, yy, Z, cmap=plt.cm.PuBuGn, alpha=0.7)    # Plot also the training points
        plt.scatter(data[:, 0], data[:, 1], c=targets, cmap=plt.cm.PuBuGn,     edgecolors='grey')    
        plt.xlabel('Sepal length')
        plt.ylabel('Sepal width')
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.xticks(())
        plt.yticks(())
        plt.title(titles[i])    
        
    plt.show()


def main():
    used_samples = 256
    generate_dataset(used_samples)
    svm_classifier()

if __name__ == "__main__":
    main()