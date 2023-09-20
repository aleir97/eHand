'''
    - Python module for pattern classification at EMG samples via support vector machines
    
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
from sklearn import svm 
from mlxtend.plotting import plot_decision_regions
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.model_selection import *
import pickle
import matplotlib as mpl
mpl.use('MacOSX')
from data_utils import *


def train_valid__svm(data, targets, safe=False):	
    linear = svm.SVC(kernel='linear', C=1, decision_function_shape='ovo')
    rbf = svm.SVC(kernel='rbf', gamma=1, C=1, decision_function_shape='ovo')
    poly = svm.SVC(kernel='poly', degree=3, C=1, decision_function_shape='ovo')
    sig = svm.SVC(kernel='sigmoid', C=1, decision_function_shape='ovo')

    # Prepare the cross-validation procedure with k-fold
    cv = KFold(n_splits=3, random_state=1, shuffle=True)
    
    # Evaluate the different models
    scores = cross_val_score(linear, data, targets, scoring='accuracy', cv=cv, n_jobs=-1)
    print('\n k - Fold Accuracy of linear model: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))

    scores = cross_val_score(poly, data, targets, scoring='accuracy', cv=cv, n_jobs=-1)
    print('\n k - Fold Accuracy of poly model: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))

    scores = cross_val_score(rbf, data, targets, scoring='accuracy', cv=cv, n_jobs=-1)
    print('\n k - Fold Accuracy of rbf model: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))

    scores = cross_val_score(sig, data, targets, scoring='accuracy', cv=cv, n_jobs=-1)
    print('\n k - Fold Accuracy of sig model: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))
    
    linear = svm.SVC(kernel='linear', C=1, decision_function_shape='ovo').fit(data, targets)
    rbf = svm.SVC(kernel='rbf', gamma=1, C=1, decision_function_shape='ovo').fit(data, targets)
    poly = svm.SVC(kernel='poly', degree=3, C=1, decision_function_shape='ovo').fit(data, targets)
    sig = svm.SVC(kernel='sigmoid', C=1, decision_function_shape='ovo').fit(data, targets)

    titles = ['Linear kernel','Polynomial kernel','RBF kernel','Sigmoid kernel']
    plt.figure()
    for i, clf in enumerate((linear, poly, rbf, sig)):
        ax = plt.subplot(2,2,i+1)
        plot_decision_regions(data, targets, clf=clf, legend=4)

        ax.set_title(titles[i])
        ax.set_xlabel("RMS at CH1")
        ax.set_ylabel("RMS at CH2")
    plt.show()

    if safe:
        if ( input('Are u sure u wanna save? YES|NO ') == 'YES' ):
            filename = './ehand_svm.sav'
            pickle.dump(linear, open(filename, 'wb'))
        else:
            exit()
    

def main():
	#data, targets = get_data(used_samples)
	#train_valid__svm(data, targets)
	
	model = pickle.load(r'D:\PROYECTO_MANO_FPGA\GIT\python\models\ehand_svm.sav')
	classification(used_samples, model)

if __name__ == "__main__":
    main()
