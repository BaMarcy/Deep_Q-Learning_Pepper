# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 11:35:00 2018

@author: MarcellBalogh
"""
from ai_B import Dqn
import matplotlib.pyplot as plt
#from joblib import load
import pepper
#clf = load('h_detection.joblib')


distances = [0, 0]
velocity = [0, 0]
reward = 0
    
brain = Dqn(32, 2, 0.9) # 1 sensor, 21 actions, gama = 0.9
actions = [0.0, 1.0]#np.arange(0, act) # action = 0 => no increment, action = 1 =>  acceleration 0.5, action = 2 => decceleration 0.5
scores = [] # initializing the mean score curve (sliding window of the rewards) with respect to time
states = []

def AI(d, v, x, y):
    global reward
    global distances
    distances[0] = d
    # specifying the global variables (the brain of the car, that is our AI)
    global brain 
     # specifying the global variables (the means of the rewards)
    global scores
    states = [d,v, 
              x[0], x[1], x[2], x[3], x[4], 
              x[5], x[6], x[7], x[8], x[9], 
              x[10], x[11], x[12], x[13], x[14],
              y[0], y[1], y[2], y[3], y[4],
              y[5], y[6], y[7], y[8], y[9],
              y[10], y[11], y[12], y[13], y[14]
              ] 
    # Getting our AI, which we call "brain", and that contains our neural network that represents our Q-function
    # playing the action from our ai (the object brain of the dqn class)
    action = brain.update(reward, states) # playing the action from our ai (the object brain of the dqn class)
     # appending the score (mean of the last 100 rewards to the reward window)
    scores.append(brain.score())
    
#    hello = clf.predict(z)
        
    if d < 1.0:  
        if v == 0:
            reward = -1 
        else:
            reward = 1
            
    elif d > 1.0:
        if pepper.touch() == True:
            if v == 0:
                reward = -1
            else:
                reward = 1
        elif v == 0:
            reward = 1
        elif v == 1:
            reward = -1   
            
    print (pepper.touch())
    print ("R: ", reward)
#    distances[1] = d
    return actions[action]

#motion = setupMotion()

a = 0.1
d = 0.0


print("Do you want to load the last model? [y/n]: ")
i = raw_input("")     
if i == "y":
    brain.load()
    print("Model's loaded.")
    print("Start.")
else:
    print("Start learning...")
    
while(1):
    try:
        pepper.IO(True)
        x = pepper.laser_reading("Right")
        y = pepper.laser_reading("Left")
#        z = [x + y  + [1.5]]
        d = pepper.sonar()
        a = AI(d, a, x, y)
        pepper.control(a, 0)
    except:
        pepper.control(0.0, 0.0)
        break

print("Do you want to save? [y/n]: ")
i = raw_input("")     
if i == "y":
    brain.save()
    print("Model's saved.")
    plt.plot(scores)
    print("Session's done.")
else:
    plt.plot(scores)
    print("Session's done.")
