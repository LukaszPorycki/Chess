import numpy as np
import matplotlib.pyplot as plt
class diffrential_equations():
    def __init__(self):
        pass
    def analitic_resolve(self,t):
        return ((2/6)*t**2-(4/6)*t**3+4)**2

    def plott(self,t,f):
        plt.plot(t,f(t))
        plt.show()

    def euler_resolve(self,h,y0,f):
        ynext = y0
        time=[]
        resolve = []
        for t in np.arange(0,1.6,0.001):
            yn=ynext
            print(yn,t)
            ynext = yn + h*f(t,yn)
            time.append(t+1)
            resolve.append(ynext)
        plt.plot(time,resolve)
        plt.show()
    def function(self,t,y):
        return (3*t-4*t**2)*np.sqrt(y)

if __name__=='__main__':
    equation =  diffrential_equations()
    equation.plott(np.linspace(0,1.6),equation.analitic_resolve)
    equation.euler_resolve(0.001,1,equation.function)

