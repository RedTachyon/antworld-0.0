from matplotlib import animation
from tqdm import tqdm
import matplotlib.pyplot as plt

from simulator import Simulator
from core import World
from viz import show_picture

ITERS = 100

sim = Simulator()

# First set up the figure, the axis, and the plot element we want to animate
fig, ax = plt.subplots()
pbar = tqdm(total=ITERS)

# animation function.  This is called sequentially
def animate(i):
    ax.cla()
    img = show_picture(sim.world, [actor.ant for actor in sim.actors])
    sim.iterate()

    pbar.update(1)
    im = ax.imshow(img)
    return im,


anim = animation.FuncAnimation(fig, animate,
                               frames=ITERS, interval=20, blit=True)

anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
