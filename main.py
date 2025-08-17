import numpy as np
import argparse
from pathlib import Path
from src import *
import os

parser = argparse.ArgumentParser(description='Shepherding simulation')
parser.add_argument('--num_agents', type=int, default=100, help='Total number of agents (helpers + leaders + followers)')
parser.add_argument('--num_helpers', type=int, default=10, help='Number of helpers')
parser.add_argument('--num_leaders', type=int, default=10, help='Number of leaders')
parser.add_argument('--helper_weight', type=float, default=20, help='Helper weight')
parser.add_argument('--leader_weight', type=float, default=40, help='Leader weight')
parser.add_argument('--follower_weight', type=float, default=1, help='Follower weight')
parser.add_argument('--exit_line', type=float, default=0.8, help='Exit line (x=exit)')
parser.add_argument('--danger_angle', type=float, default=0.5, help='Danger line angle (a in y=-ax+b)')
parser.add_argument('--danger_offset', type=float, default=0.9, help='Danger line offset (b in y=-ax+b)')
parser.add_argument('--velocity', type=float, default=0.1, help='Velocity (c)')
parser.add_argument('--rendezvous_weight', type=float, default=0.001, help='Rendezvous weight (step size)')
parser.add_argument('--num_frames', type=int, default=100, help='Number of frames for output video')
parser.add_argument('--time', type=float, default=500, help='Experiment time (time units)')

args = parser.parse_args()
n = args.num_agents
n_helpers = args.num_helpers
n_leaders = args.num_leaders
w_h = args.helper_weight
w_l = args.leader_weight
w_f = args.follower_weight
x_e = args.exit_line
a_f = - args.danger_angle
b_f = args.danger_offset
c = args.velocity
step = args.rendezvous_weight
FR = args.num_frames
T = args.time

Path('./positions').mkdir(parents=True, exist_ok=True)
Path('./videos').mkdir(parents=True, exist_ok=True)
Path('./plots').mkdir(parents=True, exist_ok=True)

folder_name = 'wl_' + str(w_l) + '_wh_' + str(w_h) + '_wf_' + str(w_f) + '_exit_' + str(x_e) + '_angle_' + str(-a_f) + '_offset_' + str(b_f)
f_name = '/c_' + str(c) + '_a_' + str(step)  + '_helpers_' + str(n_helpers) + '_leaders_' + str(n_leaders) + '_total_' + str(n)

Path('./positions/' + folder_name).mkdir(parents=True, exist_ok=True)
Path('./videos/' + folder_name).mkdir(parents=True, exist_ok=True)
Path('./plots/' + folder_name).mkdir(parents=True, exist_ok=True)

# Problem setup
# ------------------------------------------------------------------
prob = Problem(w_h, w_l, w_f, a_f, b_f, x_e) 
prob.c = c
prob.step = step
prob.n = n

# Initialize n agents randomly within the feasible region; helpers are the closest agents to danger zone
X_0, Y_0, agent_list = initialize(n,a_f,b_f,x_e, n_leaders, n_helpers)
prob.X_b = X_0
prob.Y_b = Y_0
prob.agent_list = agent_list

# Network
W = generate_W(X_0,Y_0)
prob.W = W

# Inspect agent initial locations and connectivity visually
init_plot(a_f,b_f,x_e,X_0,Y_0,W,agent_list, './plots/' + folder_name + f_name)
# ------------------------------------------------------------------

# Asynchronous clock setup
# ------------------------------------------------------------------
# Activation probabilities (sample half-normal)
lam = np.abs(np.random.normal(1,1e-1,n))
local_clock = local_time(T, lam)
clock = global_clock(local_clock)
its = len(clock)
clock_array = np.array(clock)[:,0]

# Create clock for video
video_clock = np.linspace(0, clock_array[-1], FR)
video_ticks = [np.argmin((clock_array - video_clock[frame])**2) for frame in range(FR)]
pos_x_interp = []
pos_y_interp = []

for i in range(n):
    pos_x_interp.append([])
    pos_y_interp.append([])
# ------------------------------------------------------------------

# Agent setup
# ------------------------------------------------------------------
agents = []
for i in range(n):
    agents.append(Agent(agent_list[i], i, local_clock[i], prob))
# ------------------------------------------------------------------

positions_X = np.zeros((n,its))
positions_Y = np.zeros((n,its))
    
for k in range(its):

    positions_X[:,k] = prob.X_b
    positions_Y[:,k] = prob.Y_b
    
    if k in video_ticks:
        for i in range(n):
            pos_x_interp[i].append(prob.X_b[i])
            pos_y_interp[i].append(prob.Y_b[i])

    a_i = agents[int(clock[k,-1])] # active agent
    a_i.sense_position()
    
    # update buffer
    prob.X_b[a_i.ind] = a_i.x
    prob.Y_b[a_i.ind] = a_i.y
      
    a_i.compute_consensus(prob.X_b, prob.Y_b) # calculate consensual position
    a_i.update_direction()
    a_i.update_velocity()
    a_i.counter += 1

X_name = './positions/' + folder_name + f_name + '_X.npy'
Y_name = './positions/' + folder_name + f_name + '_Y.npy'

filenum = 0
while os.path.exists(X_name):
    filenum += 1
    X_name = './positions/' + folder_name + f_name + '_X_' + str(filenum) + '.npy'
    Y_name = './positions/' + folder_name + f_name + '_Y_' + str(filenum) + '.npy'

# Save positions
np.save(X_name, positions_X)
np.save(Y_name, positions_Y)
   
prob.lims = [0,1,0,1]
# Generate video
f_name = './videos/' + folder_name + f_name
generate_video(pos_x_interp, pos_y_interp, prob, video_clock, lam, FR, f_name, n)

