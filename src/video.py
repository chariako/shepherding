import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers
from matplotlib.lines import Line2D
import numpy as np
import os

def generate_video(pos_x_interp, pos_y_interp, prob, myclock, lam, FR, f_name, n):
    
    x_e = prob.x_e
    a_f = prob.a_f
    b_f = prob.b_f

    agent_list = prob.agent_list
    markers = []
    colors = []
    for i in range(n):
        
        if agent_list[i] == 'leader':
            markers.append('>')
            colors.append('black')
        elif agent_list[i] == 'helper':
            markers.append('>')
            colors.append('red')
        else:
            markers.append('o')
            colors.append('green')
    
    legend_elements = [Line2D([0], [0], marker='>', color='white', label='leader',
                          markerfacecolor='black', markersize=15),
                    Line2D([0], [0], marker='>', color='white', label='helper',
                          markerfacecolor='red', markersize=15),
                    Line2D([0], [0], marker='o', color='white', label='follower',
                          markerfacecolor='green', markersize=15),
                     Line2D([0], [0], color='blue' , label='exit zone',
                          linestyle='--', markersize=15),
                     Line2D([0], [0], color='red' , label='danger zone',
                          linestyle='--', markersize=15)]

    Writer = writers['ffmpeg']
    writer = Writer(fps=80, bitrate=1800)

    # Axes limits
    x_max = 1.1 * prob.lims[1]
    x_min = 1.1 * prob.lims[0]
    y_max = 1.1 * prob.lims[3]
    y_min = 1.1 * prob.lims[2]
    
 
    fig, ax = plt.subplots(figsize=(7, 7), dpi=120)
    plt.tight_layout()

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('[m]')
    ax.set_ylabel('[m]')
    ax.set_title('t = {:.2f} sec'.format(myclock[0]))

    
    ax.legend(handles=legend_elements,loc='upper right')
   

    # plot fire
    xxs = np.linspace(x_min, x_max, 100)
    plt.plot(xxs, a_f * xxs + b_f, '--', color='red', lw=4)
    plt.fill([x_max, x_max, -(b_f - y_max)/a_f],
             [y_max, a_f * x_max + b_f, y_max], color='red', alpha=.5)

    # plot exit
    yys = np.linspace(y_min,y_max, 100)
    plt.plot(x_e * np.ones_like(yys), yys, '--', color='blue', lw=4)
    plt.fill([x_e, x_max, x_max, x_e],
             [y_max, y_max, y_min, y_min], color='blue', alpha=.5)

    print('Creating video...')
    print('Total frames: ', FR)

    line = []

    for i in range(n):

        my_line, =  ax.plot([], [], marker=markers[i], color=colors[i], ms=12)
        line.append(my_line)

    def init():

        plt.tight_layout()
    
        for i in range(n):
            line[i].set_data([], [])
    
        return line

    def update(i):

        plt.tight_layout()
    
        if not i % 20:
            print('Current frame: ', i)
    
        for j in range(n):
            line[j].set_data(np.array([pos_x_interp[j][i]]),np.array([pos_y_interp[j][i]]))
    
        if i:
            for j in range(n):
                newsegm, = ax.plot([pos_x_interp[j][i-1], pos_x_interp[j][i]], [pos_y_interp[j][i-1], pos_y_interp[j][i]],
                                   alpha=.2,color=colors[j])
    
        ax.set_title('t = {:.2f} sec'.format(myclock[i]))
    
        return line

    ani = FuncAnimation(fig, update, init_func=init, frames=FR, interval=15)

    name = f_name + '.mp4'
    filenum = 0
    while os.path.exists(name):
        filenum += 1
        name = f_name + '_' + str(filenum) + '.mp4'

    ani.save(name, writer=writer, dpi=200) 


