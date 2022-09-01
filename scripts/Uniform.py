"""

@author: andrewkof

Run example:
python3 Uniform.py --c=0.2

Visit "Run examples" section of README for more info about the default values and choices.

"""
import numpy as np                                                                     # Import required libraries
import scipy
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.optimize import minimize_scalar

def check_positive(value):
    ivalue = float(value)
    if ivalue < 0 or ivalue > np.e - 2:
        raise argparse.ArgumentTypeError("%s, c value must be positive and less than e-2, thus 1-b ≥ 0." % value)
    return ivalue


parser = argparse.ArgumentParser(description='Uniform')
parser.add_argument('--c', default=0.5, type=check_positive, help='[float] Parameter of distribution P')
args = parser.parse_args()
c = args.c
x = np.linspace(0,2,2000)                                                               # 2000 equidistant points in [0,2]

def f(b):                                                                               # Define function f(b)
    global c
    return np.exp(1-b) - (1-b) - 1 - c

def fprime(b):                                                                          # Define f'(b)
    return -np.exp(1-b)+1

b = scipy.optimize.root_scalar(f, x0=0.1, fprime=fprime, method='newton').root          # Minimum root of f function using newtons method

def gama(x, a):                                                                         # Define 'gama star' function in [a,1] for 0 ≤ a < 1
    result = []
    global b,c
    for i in x:
        if a <= i <= b:
            result.append(1/(1+c))
        elif b < i <= 1:
            result.append(np.exp(i-b)/(1+c))
        else:
            result.append(0.0)
    return result

def uniform_distribution(x, a, b):                                                     # Define Uniform Distribution in [a,b]
    result = []
    for i in x:
        if a <= i <= b :
            result.append(1/(b-a))
        else:
            result.append(0.0)
    return result

def Multiply(x,num):
    return [point*num for point in x]

def sum_lists(L1, L2):
    return [L1[i]+L2[i] for i in range(len(L1))]


Frames = np.linspace(0,1,50)

fig, ax = plt.subplots()                                                 # Make invisible the top and right lines of
ax.spines["right"].set_visible(False)                                    # the plot frame
ax.spines["top"].set_visible(False)
ax.set_xlabel('x', fontsize = 12)
ax.set_ylabel('y', fontsize = 12, rotation='horizontal')

ax.plot((1), (0), ls="", marker=">", ms=10, color="k",transform=ax.get_yaxis_transform(), clip_on=False)    # Create 2 arrows
ax.plot((0), (1), ls="", marker="^", ms=10, color="k",transform=ax.get_xaxis_transform(), clip_on=False)

plt.xticks([0, b, 1, 1+c])
plt.yticks([1/(1+c), 1])
ax.set_xticklabels([0, 'b','1','1+c'])
ax.set_yticklabels(["$\\frac{1}{1+c}$", '1'])


ax.yaxis.set_label_coords(-0.025,0.9)
ax.xaxis.set_label_coords(0.9, -0.025)
plt.xlim(0, 2)                                                                                             # Limit frame (x,y) = [0,2]x[0,2]
plt.ylim(0, 2)

def animate(i):
    global x
    if i < 50:
        plt.title('P => $\eta$*', fontsize=12)
        plt.suptitle('Mass Transport', fontweight="bold", fontsize=14)
        y = sum_lists(Multiply(uniform_distribution(x,0,1+c), 1-Frames[i]), Multiply(gama(x,0), Frames[i]))         # Apply formula
        line.set_data(x,y)
    elif i > 50:
        plt.title('$\eta$* => Q ', fontsize=12)
        plt.suptitle('Mass Redistribution',fontweight="bold",fontsize=14)
        y = sum_lists(Multiply(uniform_distribution(x, 0, 1), Frames[i-50]), Multiply(gama(x,0), 1-Frames[i-50]))   # Apply formula
        line.set_data(x, y)
    return line,

line, = ax.plot([], [], lw=2, color='red')
anim = animation.FuncAnimation(fig, animate, frames = 100,interval = 100)                                        # Create animation
anim.save('Uniform.gif', writer = animation.PillowWriter(fps=60))                                                # Save animation on current directory
#plt.show()
