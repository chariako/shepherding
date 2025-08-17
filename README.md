# Agent-based simulation of an emergency evacuation scenario

## Overview
This project generates a multi-agent-based simulation of a 2-D emergency evacuation scenario with three objectives:

1. All agents must be lead away from a danger zone, denoted by the half-plane
   
$$
y \geq -ax + b,
$$

for some positive scalars $a$ and $b$.

2. All agents must be lead to a safety zone, denoted by the half plane
   
$$
x \geq e,
$$

for some positive scalar $e$. 

3. All agents must remain in close proximity during evacuation (rendezvous).

## Agent types
- Leader (L): The goal of L agents is to guide all agents to the safety zone $x \geq e$. The objective function of L agents is given by

$$
f_L(x,y) = \frac{w_L}{2} (x - e - d_e)^2,
$$

where $w_L$ is a positive weight, and $d_e$ is a small positive displacement ensuring that agents cross the boundary of the safety zone.

- Helper (H): The goal of H agents is to lead all agents away from the danger zone. By default, they are the agents located closest to the danger zone at the start of the simulation. The objective function of H agents is given by

$$
f_H(x,y) = - \frac{w_H}{2} \ln(b - y - a x),
$$

where $w_L$ is a positive weight and $\ln(\cdot)$ is the natural logarithm.

- Follower (F): The goal of F agents is to remain close to their original locations $(x_0,y_0)$ at the start of the simulation, modeling the tendency to remain in place during real-world emergency evacuations. The objective function of F agents is given by

$$
f_F(x,y) = \frac{w_F}{2} (x-x_0)^2 + \frac{w_F}{2} (y-y_0)^2,
$$

where $w_F$ is a positive weight.

## Global objective
Let $(x_i,y_i)$ be the position of the $i^{th}$ agent on the 2-D plane and denote the sets of L, H and F agents as $S_L$, $S_H$ and $S_F$, respectively. The global objective is given by

$$
\sum_{i \in S_L} f_L(x_i,y_i) + \sum_{i \in S_H} f_H(x_i,y_i) + \sum_{i \in S_F} f_F(x_i,y_i) + \frac{1}{2\alpha} (\text{rendezvous penalty})
$$

where $\alpha$ is a positive scalar, and the rendezvous penalty is a quadratic penalty ensuring that objective (3) is met. Lower values of the parameter $\alpha$ result in agents staying in closer proximity to each other.

## Agent communication
During the simulation, each agent can communicate with all agents initialized within a radius $R >0$ from the agent's initial position. Agent positions are initialized randomly. The connectivity radius $R$ is set to the smallest scalar ensuring a connected graph at initialization. 

## Usage
To run the simulation using command line, navigate to the project folder and type:

`python main.py <args>`

## Arguments
- `--num_agents`: Total number of agents, including L, H and F types (type:`int`, default:`100`)
- `--num_helpers`: Total number of H agents (type:`int`, default:`10`)
- `--num_leaders`: Total number of L agents (type:`int`, default:`10`)
- `--helper_weight`: Weight $w_H$ of H agent objective function (type:`float`, default:`20`)
- `--leader_weight`: Weight $w_L$ of L agent objective function (type:`float`, default:`40`)
- `--follower_weight`: Weight $w_F$ of F agent objective function (type:`float`, default:`1`)
- `--exit_line`: Parameter "e" in the safety zone half-plane $x \geq e$ (type:`float`, default:`0.8`)
- `--danger_angle`: Parameter "a" in the danger zone half-plane $y \geq -ax + b$ (type:`float`, default:`0.5`)
- `--danger_offset`: Parameter "b" in the danger zone half-plane $y \geq -ax + b$ (type:`float`, default:`0.9`)
- `--velocity`: Agent velocity (type:`float`, default:`0.1`)
- `--rendezvous_weight`: Weight $\alpha$ of the rendezvous penalty (type:`float`, default:`0.1`)
- `--num_frames`: Number of frames for output video (type:`int`, default:`100`)
- `--time`: Total time of the simulation in artificial time units, i.e., not corresponding to actual run time (type:`float`, default:`500`)

## Outputs
Output files follow the convention below:

*filename = c\_\<velocity>\_a\_\<rendezvous_weight>\_helpers\_\<num_helpers>\_leaders\_\<num_leaders>\_total\_\<total_agents>*

*foldername = wl\_\<leader_weight>\_wh\_\<helper_weight>\_wf\_\<follower_weight>\_exit\_\<e>\_angle\_\<a>\_offset\_\<b>*

- A video of the simulation (\<filename>.mp4), stored in ./videos/foldername/
- A snapshot of the intialization state, depicting initial positions and the communication graph topology (\<filename>\_init.png), stored in ./plots/foldername/
- Coordinates of all agents on the 2-D plane throughout the simulation (\<filename>\_X.npy, \<filename>\_Y.npy), stored in ./positions/foldername/



