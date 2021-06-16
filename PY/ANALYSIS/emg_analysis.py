import matplotlib.pyplot as plt
import numpy as np
from numpy.core.fromnumeric import mean
 
#Decimation
flsig = np.genfromtxt('D:\PROYECTO_MANO_FPGA\GIT\PY\ANALYSIS\signal.txt', delimiter='\n').astype(int)
#flsig = flsig[1:1001:2]
flsig = flsig[1:1001:10]

restsig =np.genfromtxt('D:\PROYECTO_MANO_FPGA\GIT\PY\ANALYSIS\signal2.txt', delimiter='\n').astype(int)
restsig = restsig[1:1001:10]

n = np.arange(1,101)

meanfl = mean(flsig) 
print(meanfl)
meanrest =  mean(restsig)
print(meanrest)


plt.stem(n, flsig)

plt.figure()
plt.stem(n, restsig)

plt.show()
