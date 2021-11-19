#!/usr/bin/env python
from numpy.lib.financial import rate
import rospy
import time
from multiprocessing import Process, process
import actionlib
from battery_simulator.msg import Battery_SimAction, Battery_SimGoal

def batterySim():
    pass

def goal_clbck(goal):
    rate = rospy.Rate(2) # Relog de ROS
    proceso = Process(target=batterySim)
    proceso.start()
    time.sleep(1) # Nos esperamos un segundo del sistema
    if goal.charge_state == 0:
        rospy.set_param('/battery_sim/BatteryStatus',goal.charge_state)
    elif goal.charge_state == 1:
        rospy.set_param('/battery_sim/BatteryStatus',goal.charge_state)
        

if __name__ == '__main__':
    rospy.init_node('BatterySimServer')
    server = actionlib.SimpleActionServer('battery_simulator',Battery_SimAction,goal_clbck,False)
