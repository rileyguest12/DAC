import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
'''
    This is an actual problem I did in my diff eq class.
    -------------------------------------------------------------
    Newton's law of cooling states that the temperature of an object
    changes at a rate proportional to the difference between its temperature
    and that of its surroundings. Suppose that the temperature of a cup of coffee obeys
    Newton's law of cooling. Let k>0 be the constant of proportionality.
    Assume the coffee has a temperature of 210 degrees Fahrenheit when freshly poured,
    and 3 minutes later has cooled to 196 degrees in a room at 76 degrees.
'''

''' 
    Define dT/dt, find T(t)
    When you freshly pour @ T(0) = 210), T(3) = 196, Room temp = 76 degrees 
    The rate of change of temperature to time (dTemp/dtime) = -k(T-76)  
    The value of k  = 0.03678
'''
def dTdt(temp, time):           # function that returns dT/dt
    k = 0.03678                 # coefficient k
    dtempdtime = -k*(temp-76)   # dT/dt
    return dtempdtime           # returns dT/dt

y0 = 210                        # initial conditions or T0
t = np.arange(0, 60, .1)        # time range, note this uses the np.arange, just returns a range of numbers
T = 76+134*np.exp(-0.03678*t)   # The actual initial value problem
y = -0.03678*(T-76)             # declaring solution to IVP
T2 = odeint(dTdt, y0, t)        # using odeint method to solve dT/dt

plt.style.use('bmh')            # this changes the plotting style, 'dark_background' looks nice, so does 'seaborn'.
plt.plot(t, T2, 'r--')                 # plotting Temperature vs time, notice T2 and T are the same, but one uses the solver, similar to ode45 in matlab
plt.xlabel('Time (Minutes)')    # labeling x axis
plt.ylabel("Coffee Temperature (F)")   # labeling y axis
plt.title("Coffee Temperature vs. time\n"      # adding a title
          '$T(0)=210 F$' "\t" '$\dfrac{dT}{dt}=-k(T-76)$') # this is LaTEX
plt.show() # this is the command to have the plot show up