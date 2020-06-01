import numpy as np
import matplotlib.pyplot as plt

def leastSquaresNp(vectorT, signal):
    leastSquares = np.polyfit(vectorT, signal, 1)
    lineLeastSquares = vectorT*leastSquares[0] + leastSquares[1]
    
    return lineLeastSquares

def leastSquares(vectorT, signal):
    ''' 
    This function recieves a time (vectorT) array as the x axis, 
    the signal you want to aproximate (signal) as the y axis and 
    returns an array with the values for the y axis of the
    adjusted line by the least squares method.
    '''
    n = len(signal)
    L = (1 / n) * np.cumsum(signal)
    t = (1 / n) * np.cumsum(vectorT)
    m = 1 # Se fijó un valor de 1 por que no sabemos que significa dicha variable. Sabemos que no es correcto porque no dan los resultados.
    
    b = (np.cumsum(signal * vectorT) - m * t * L)/(np.cumsum(vectorT ** 2) - m * t ** 2)
    a = L - b * t
    
    lineLeastSquares = vectorT * b + a
    
    return lineLeastSquares

#--------------------TESTING----------------------------------------

x = np.flip(np.arange(-20, -10, 0.5)) + 0.2 * np.random.randn(20)
h = np.flip(np.arange(-10, 0, 0.25) + 0.6 * np.random.randn(40))
y = np.hstack((h,x))
t = np.arange(0, len (y))

cuad1 = leastSquaresNp(t, y)
cuad2 = leastSquares(t, y)

plt.plot(t, y)
plt.plot(t, cuad1)
plt.plot(t, cuad2)
plt.ylim(-20,0)



    
