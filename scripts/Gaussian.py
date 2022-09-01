"""

@author: andrewkof

Run example:
python3 Gaussian.py --m1=1.5 --sd1=0.8 --m2=3.0 --sd2=1.0

Visit "Run examples" section of README for more info about the default values and choices.

"""
import numpy as np                                                                                            # Import required libraries
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

# -------------------
# input arguments
# -------------------
parser = argparse.ArgumentParser(description='Gaussian')
parser.add_argument('--m1', default=1.0, type=float, help='[float] Mean of distribution P')
parser.add_argument('--sd1', default=0.5, type=float, help='[float] Standard deviation of distribution P')
parser.add_argument('--m2', default=3.0, type=float, help='[float] Mean of distribution Q')
parser.add_argument('--sd2', default=1.0, type=float, help='[float] Standard deviation of distribution Q')

args = parser.parse_args()
mean1 = args.m1
sd1 = args.sd1
mean2 = args.m2
sd2 = args.sd2

def normal_dist(x , mean , sd):                                                                    # Define Normal Distribution Function
    prob_density = 1/(np.sqrt( 2*(np.pi)* sd**2)) * np.exp(-0.5*((x-mean)/sd)**2)
    return prob_density


def check_case(sd1,sd2):                                                                          # Recognise the case
    k = 1/sd1**2 - 1/sd2**2
    if -1 <= k <= 1:
        return sd1, 'case_1'
    elif k > 1:
        return sd2 / np.sqrt(1+sd2**2), 'case_2'
    return sd2 / np.sqrt(1-sd2**2), 'case_3'


mean_star = mean2
sd_star, case = check_case(sd1, sd2)
x = np.linspace(mean1-5,mean2+5,2000)
fig = plt.figure()
ax = plt.axes()
ax.spines["right"].set_visible(False)                                                                         # Make invisible the top and right lines of
ax.spines["top"].set_visible(False)                                                                           # the frame

plt.xticks([mean1,mean2])
ax.set_xticklabels(['$μ_1$','$μ_2$'])                                                                         # Set x,y labels
ax.set_xlabel('x', fontsize = 12)
ax.set_ylabel('y', fontsize = 12, rotation='horizontal')

ax.yaxis.set_label_coords(-0.1,0.9)                                                                           # Position of x,y labels in frame
ax.xaxis.set_label_coords(0.9, -0.025)
ax.plot((1), (0), ls="", marker=">", ms=10, color="k",transform=ax.get_yaxis_transform(), clip_on=False)      # Create 2 arrows on x,y axis
ax.plot((mean1-5), (1), ls="", marker="^", ms=10, color="k",transform=ax.get_xaxis_transform(), clip_on=False)

plt.xlim(mean1-5,mean2+5)                                                                                               # Limit frame (x,y) = [-5,11]x[0,1]
plt.ylim(0, max(1/(np.sqrt(2*np.pi)*sd1), 1/(np.sqrt(2*np.pi)*sd2)))

Frames = np.linspace(0,1,50)                                                                                  # 50 equidistant frames on [0,1]
def animate(i):
    if i < 50 :
        plt.title('P => $\eta$*',fontsize=12)
        plt.suptitle('Mass Redistribution', fontweight="bold", fontsize=14)
        y = (1-Frames[i]) * normal_dist(x,mean1,sd1) + Frames[i] * normal_dist(x,mean_star,sd_star)           # Apply formula
        line.set_data(x,y)                                                                                    # Update data
    elif i > 50:
        plt.title('$\eta$* => Q',fontsize=12)
        plt.suptitle('Mass Transport', fontweight="bold", fontsize=14)
        y = (1-Frames[i-50]) * normal_dist(x,mean_star,sd_star) + Frames[i-50] * normal_dist(x,mean2,sd2)     # Apply formula
        line.set_data(x,y)
    return line,

line, = ax.plot([], [], lw=2, color='red')
anim = animation.FuncAnimation(fig, animate, frames=100, interval=100)

anim.save('/Users/andrew_kwf/Desktop/'+'Gaussian_' + case + '.gif', writer=animation.PillowWriter(fps=60))   # Create animation
plt.show()
# HTML(anim.to_html5_video())
