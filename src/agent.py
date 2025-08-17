import numpy as np

class Agent:

    def __init__(self, agent_type, ind, local_clock, prob):

        ## Agent type: helper, follower, leader
        self.agent_type = agent_type

        ## Agent index
        self.ind = ind
        
        ## Local clock
        self.local_clock = local_clock
        self.counter = 0

        # Problem parameters
        self.W = prob.W  # consensus matrix
        self.w_d = self.W[self.ind,self.ind]
        self.w_h = prob.w_h  # helper weight
        self.w_l = prob.w_l  # leader weight
        self.w_f = prob.w_f # fire weight
        
        ## fire coordinates
        self.a_f = prob.a_f 
        self.b_f = prob.b_f  
        
        self.x_e = prob.x_e  # exit location

        ## Initial location
        self.x_0 = prob.X_b[self.ind]
        self.y_0 = prob.Y_b[self.ind]

        ## Current location
        self.x = prob.X_b[self.ind]
        self.y = prob.Y_b[self.ind]

        ## Location history
        self.x_hist = []
        self.y_hist = []

        ## Velocity (gradient norm)
        self.g_norm = []
        
        ## Direction
        self.d_x = 0
        self.d_y = 0
        
        self.c = prob.c
        self.step = prob.step
        
    
    ## Gradient of x coordinate
    def g_x(self):

        if self.agent_type == 'helper':

            return self.w_h * self.a_f / (-self.y - self.a_f * self.x + self.b_f)

        elif self.agent_type == 'follower':

            return self.w_f * (self.x - self.x_0)

        elif self.agent_type == 'leader':

            d_e = 0.2

            return self.w_l * (self.x - self.x_e - d_e)
        
    # Gradient of y coordinate
    def g_y(self):

        if self.agent_type == 'helper':

            return self.w_h / (-self.y - self.a_f * self.x + self.b_f)

        elif self.agent_type == 'follower':

            return self.w_f * (self.y - self.y_0)

        elif self.agent_type == 'leader':

            return 0

    def sense_position(self):
        
        if self.counter == 0:
            dt = 0
        else:
            dt = self.local_clock[self.counter][0] - self.local_clock[self.counter - 1][0]
    
        self.x += self.c * dt * self.d_x
        self.y += self.c * dt * self.d_y

    def update_history(self):
        
            self.x_hist.append(self.x)
            self.y_hist.append(self.y)

    def compute_consensus(self, X_b, Y_b):

        self.x_w = np.dot(self.W[self.ind, :], X_b) 
        self.y_w = np.dot(self.W[self.ind, :], Y_b)

    def update_direction(self):
        
        new_dx = self.x_w - self.step * self.g_x() - self.x
        new_dy = self.y_w - self.step * self.g_y() - self.y
        
        self.d_x = new_dx
        self.d_y = new_dy
        
    def update_velocity(self):
        
        self.g_norm.append(self.c * np.sqrt(self.d_x**2 + self.d_y**2))

        