#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 09:39:34 2018

@author: marcell
"""
#from naoqi import ALProxy
import qi
import sys
import argparse
from math import sqrt

parser = argparse.ArgumentParser()
parser.add_argument("--ip", type=str, default="192.168.1.2",
                        help="Robot IP address")
parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
args = parser.parse_args()
session = qi.Session()
try:
    session.connect("tcp://" + args.ip + ":" + str(args.port))
except RuntimeError:
    print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
    sys.exit(1)
    
memory_service = session.service("ALMemory")
leds_service = session.service("ALLeds")

def IO(on = True):
    bg_move = session.service('ALBackgroundMovement')   
    awe = session.service('ALBasicAwareness')
    if (on):
        bg_move.setEnabled(False)
        awe.pauseAwareness()
    else:
        bg_move.setEnabled(False)
        awe.resumeAwareness()

def setupMotion():
    motion = session.service("ALMotion")
    motion.setStiffnesses('Body', 2.0)
    return motion     

def control(val1, val2):
    motion = setupMotion()
    global target_side_vel
    motion.move(val1, val2, 0)
    print (val1, val2, 0)
    
def sonar(): 
    sonar_back = round(memory_service.getData("Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value"), 2)
    return  sonar_back
    
def laser_reading(side):
    call_base = 'Device/SubDeviceList/Platform/LaserSensor/'+side+'/Horizontal/Seg'
    segments = []   
    for segment in range(1, 16):
        if segment < 10:
            call_x = call_base + '0' + str(segment) + '/X/Sensor/Value'
            call_y = call_base + '0' + str(segment) + '/Y/Sensor/Value'
        else:
            call_x = call_base + str(segment) + '/X/Sensor/Value'
            call_y = call_base + str(segment) + '/Y/Sensor/Value'
        value_x = round(memory_service.getData(call_x), 2)
        value_y = round(memory_service.getData(call_y), 2)
        dist = round(sqrt((value_x**2) + (value_y**2)), 2)
        segments.append(dist)
    return segments   

def touch():
    #value = True
    value1 = memory_service.getData('Device/SubDeviceList/Head/Touch/Front/Sensor/Value')
    value2 = memory_service.getData('Device/SubDeviceList/Head/Touch/Middle/Sensor/Value')
    value3 = memory_service.getData('Device/SubDeviceList/Head/Touch/Rear/Sensor/Value')
    if value1 == 1.0 or value2 == 1.0 or value3 == 1.0:
        value = True
    else:
        value = False
    return value