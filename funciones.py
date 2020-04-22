# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt


def impulsos(arrayParametros, inicio, fin):
    x = np.arange(inicio,fin,1)
    y = np.zeros(len(x))
    for i in range (0, len(arrayParametros)):
        paramsi = arrayParametros[i]
        y[paramsi[0]] = paramsi[1]
        i += 1
    return y
        
y = impulsos([[4,1],[0,-1]],0,5)
x = np.arange(0,6,1)

plt.plot(y)
