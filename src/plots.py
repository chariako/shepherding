import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os

def init_plot(a_f,b_f,x_e,X_0,Y_0,W,agent_list, f_name):
    
    n = len(X_0)
    
    xx = np.linspace(0,1,100)
    yy = np.linspace(0,1,100)
    plt.plot(xx,a_f * xx + b_f, color='r')
    plt.plot(x_e * np.ones(100),yy, color='b')
    for i in range(n):
        if agent_list[i] == 'follower':
            agent_color = 'g'
        elif agent_list[i] == 'leader':
            agent_color = 'black'
        else:
            agent_color = 'm'
        plt.plot(X_0[i],Y_0[i],'o', color=agent_color)

    for i in range(n):
        
        for j in set(range(n)) - set(range(i+1)):
            
            if W[i,j] > 0:
                
                plt.plot([X_0[i],X_0[j]],[Y_0[i],Y_0[j]], ls='--', color='gray')
                
    legend_elements = [Line2D([0], [0], marker='o', color='white', label='leaders',
                          markerfacecolor='black', markersize=8),
                    Line2D([0], [0], marker='o', color='white', label='helpers',
                          markerfacecolor='m', markersize=8),
                    Line2D([0], [0], marker='o', color='white', label='followers',
                          markerfacecolor='green', markersize=8),
                     Line2D([0], [0], color='blue' , label='exit zone',
                          linestyle='-', markersize=15),
                     Line2D([0], [0], color='red' , label='danger zone',
                          linestyle='-', markersize=15)]
    
    plt.legend(handles=legend_elements,loc='upper right',fontsize=11)

    name = f_name + '_init.png'
    filenum = 0
    while os.path.exists(name):
        filenum += 1
        name = f_name + '_init_' + str(filenum) + '.png'

    plt.savefig(name, dpi=200)
