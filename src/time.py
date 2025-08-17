import numpy as np

def local_time(T, lambdas):

    t = []  # time dictionary

    for i in range(len(lambdas)):
        
        t_list = np.random.exponential(1/lambdas[i],int(lambdas[i] * T))
        t_list = np.cumsum(t_list)
        ticks_i = [(tick, i) for tick in t_list]

        t.append(ticks_i)

    return t

def global_clock(time):

    gb_clock = []

    for item in time:

        gb_clock = gb_clock + item

    gb_clock.sort()

    return np.array(gb_clock)
