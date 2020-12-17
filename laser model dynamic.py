''' Animated graphs showing 3 level laser vs 4 level laser'''
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import matplotlib.animation as animation

linewidth = 2.0
threshold = 0.25
Trad = 1
t43 = 0.5
beta = 0
n = 1
x = np.linspace(0, 5, 250)
Wp = x
y = ((1-beta)*n*Wp*Trad-1)/((1+2*beta)*n*Wp*Trad+1)
y2 = ((1-beta)*n*Wp*Trad)/(1+(1+beta+(2*t43/(Trad))*n*Wp*Trad))
fig, ax = plt.subplots()
line1, = ax.plot(x, y, linewidth=linewidth, label='3 Level Laser')
line2, = ax.plot(x, y2, linewidth=linewidth, label='4 Level Laser')

def update(num, x, y, y2, line1, line2):
    line1.set_data(x[:num], y[:num])
    line2.set_data(x[:num], y2[:num])
    return [line1, line2]

ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, y, y2, line1, line2], interval=20, blit=True)
ax.set_xlabel('Normalized Pump Rate')
ax.set_ylabel('Normalized Population Inversion')
plt.axhline(0.25, color='black', linewidth=2.0)
plt.grid(True)
plt.legend(loc='center right')
plt.title("3 Level Laser Vs. 4 Level Laser Population Inversion\nNote: Y axis; an example of why 3 Level Lasers\n"
              "need more pump energy to start a population inversion")
plt.tight_layout()
plt.show()