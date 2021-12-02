#!/usr/bin/env python
from numpy.lib.financial import rate
import rospy
import time
from multiprocessing import Process, process
import actionlib
from battery_simulator.msg import Battery_SimAction, Battery_SimGoal, Battery_SimResult, Battery_SimFeedback

def batterySim():
    battery_lavel = 100
    result = Battery_SimResult()
    while not rospy.is_shutdown():
        if rospy.has_param('/battery_sim/BatteryStatus'):
            time.sleep(1)
            param = rospy.get_param('/battery_sim/BatteryStatus')
            if param == 1:
                if battery_lavel == 100:
                    result.battery_status = 'Cargada'
                    server.set_succeeded(result)
                    break
                else:
                    battery_lavel +=1
                    result.battery_status = 'Cargando'
                    rospy.loginfo('Cargando... actualmente %s', battery_lavel)
                    time.sleep(4)
            elif param == 0:
                battery_lavel -= 1
                rospy.logwarn('Descargando... Actualmente %s', battery_lavel)
                time.sleep(2)


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
    server.start()
    rospy.spin()
