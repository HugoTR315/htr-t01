#! /usr/bin/env python
from _typeshed import Self
import rospy
import actionlib
from actionlib import GoalStatus
from geometry_msgs.msg import PointStamped, Point

class RobotMoveActionServer():
    def __init__(self):
        # Descricion actual del robot
        self._ipose = PointStamped() # Posicion
        self._iorient_rpy = Point() # Orientacion
        # Variables de control para la maquina del robot
        self._state_code = 0
        self._code_states = ['STOP','TWIST','GO','GOAL']
        # Variables de control para mover y alcanzar la meta
        self._goal = None # Definimos la meta

def main():
    pass

if __name__=='__main__':
    main()