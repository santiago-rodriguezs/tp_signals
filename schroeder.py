import scipy as sp
import numpy as np
def schroeder(iR, end):
    t = sp.Symbol('t')
    integrate_sch = sp.integrate(iR**2, (t, 0, np.inf)) - sp.integrate(iR**2, (t, 0, end))
    
    return integrate_sch

    sch = np.cumsum(np.abs(iR)**2)

    #sch = np.cumsum(abs_signal[::-1]**2)[::-1]
    
