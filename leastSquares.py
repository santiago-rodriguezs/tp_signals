import numpy as np
import matplotlib.pyplot as plt

def leastSquaresNp(time, signal):
    leastSquares = np.polyfit(time, signal, 1)
    lineLeastSquares = time*leastSquares[0] + leastSquares[1]
    
    return lineLeastSquares

def leastSquares(vectorT, signal):
    n = len(signal)
    L = (1 / n) * np.cumsum(signal)
    t = (1 / n) * np.cumsum(vectorT)
    m = 1
    
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



    