"""

@author: andrewkof

Run example:
python3 Dirac_case2.py --h=0.3


Visit "Run examples" section of README for more info about the default values and choices.

"""
import matplotlib.pyplot as plt                                                                                 # Import required libraries
import matplotlib.animation as animation
import numpy as np
import argparse

# -------------------
# input arguments
# -------------------
parser = argparse.ArgumentParser(description='Dirac')
parser.add_argument('--h', default=0.1, type=float, help='[float] Position of η(x2) from 0.5')
args = parser.parse_args()
h = args.h

arrow1_goes_up = np.linspace(1/2-h,1/3,20)                                                                      # 20 equidistant frames for each arrow
arrow1_goes_down = np.linspace(1/2-h,1/2,20)[::-1]
arrow2_goes_up = np.linspace(1/2,1/2+h,20)
arrow2_goes_down = np.linspace(1/3, 1/2+h, 20)[::-1]
arrow3_goes_up = np.linspace(0, 1/3, 20)



fig, ax = plt.subplots()

ax.spines["right"].set_visible(False)                                                                           # Make invisible the top and right lines of
ax.spines["top"].set_visible(False)                                                                             # the frame

ax.plot((1), (0), ls="", marker=">", ms=10, color="k",transform=ax.get_yaxis_transform(), clip_on=False)        # Create 2 arrows on x,y axis
ax.plot((-0.1), (1), ls="", marker="^", ms=10, color="k",transform=ax.get_xaxis_transform(), clip_on=False)

plt.xlim(-0.1,1.5)                                                                                              # Limit frame, (x,y) = [-0.1,1.5]x[0,1]
plt.ylim(0,1)

patch1 = plt.Arrow(0,0,0,1/2,width=0.1,color='red')                                                             # Initialize 3 arrows
patch2 = plt.Arrow(0.5,0, 0,1/2,width=0.1,color='red')
patch3 = plt.Arrow(1,0, 0,0,width=0.1,color='red')
ax.add_patch(patch1)
ax.add_patch(patch2)
ax.add_patch(patch3)

plt.plot([-1, 2],[1/3,1/3],'--', linewidth=1,color = 'black')                                                   # Plot lines: y=1/3, y=1/2, y=2/3
plt.plot([-1, 2],[1/2,1/2],'--', linewidth=1,color = 'black')
plt.plot([-1, 2],[2/3,2/3],'--', linewidth=1,color = 'black')
plt.plot([-1, 2],[1/2+h,1/2+h],'--', linewidth=1,color = 'black')

plt.xticks([0,1/2])                                                                                           # Set x,y ticks
ax.set_xticklabels(['$x_1$','$x_2$'])
plt.yticks([0,1/3,1/2,2/3,1])
plt.yticks([0,1/3,1/2,1/2+h,2/3,1])
ax.set_yticklabels([0,'1/3','1/2','$\eta^*(x_2)$','2/3', 1])

def animate(i):
    global patch1,patch2,patch3
    ax.patches.remove(patch1)                                                                                   # Remove arrows to clear graph for next step
    ax.patches.remove(patch2)
    if i < 20:                                                                                                  # First 20 frames is "Mass Redistribution"

        plt.title('P => $\eta$*',fontsize=12)
        plt.suptitle('Mass Redistribution', fontweight="bold", fontsize=14)
        # fig.suptitle('Mass Redistribution',fontweight="bold",fontsize=14)
        patch1 = plt.Arrow(0,0,0,arrow1_goes_down[i],width=0.1,color='red')
        patch2 = plt.Arrow(0.5,0, 0,arrow2_goes_up[i],width=0.1,color='red')
        ax.add_patch(patch1)
        ax.add_patch(patch2)
        return patch1,patch2

    elif i >= 20:                                                                                               # Last 20 frames is "Mass Transfer"
        ax.patches.remove(patch3)
        plt.title('$\eta$* => Q',fontsize=12)
        plt.suptitle('Mass Transport', fontweight="bold", fontsize=14)
        # fig.suptitle('Mass Transfer',fontweight="bold", fontsize=14)
        plt.xticks([0,1/2,1])                                                                                   # Update xticks (x3 added)
        ax.set_xticklabels(['$x_1$','$x_2$','$x_3$'])
        patch1 = plt.Arrow(0,0,0,arrow1_goes_up[i-20],width=0.1,color='red')
        patch2 = plt.Arrow(0.5,0, 0,arrow2_goes_down[i-20],width=0.1,color='red')
        patch3 = plt.Arrow(1,0,0,arrow3_goes_up[i-20],width=0.1,color='red')
        ax.add_patch(patch1)
        ax.add_patch(patch2)
        ax.add_patch(patch3)

        return patch1,patch2,patch3

anim = animation.FuncAnimation(fig, animate, frames = 40,interval = 100)                                        # Create animation
anim.save('/Users/andrew_kwf/Desktop/'+'dirac_case2.gif', writer= animation.PillowWriter(fps=60))# Create animation

plt.show()
# HTML(anim.to_html5_video())
