#! /usr/bin/env python
from _typeshed import Self
import rospy
import actionlib
from actionlib import GoalStatus
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PointStamped, Point, Twist
from robot_move.msg import RobotMoveMsg_Action, RobotMoveMsg_Feedback
import math



class RobotMoveActionServer():
    def __init__(self,base_lin_vel = 0.2, base_ang_vel=0.2,min_dist = 0.05, yaw_tolerance = math.pi/90):
        # Descricion actual del robot
        self._ipose = PointStamped() # Posicion
        self._iorient_rpy = Point() # Orientacion
        # Variables de control para la maquina del robot
        self._state_code = 0
        self._code_states = ['STOP','TWIST','GO','GOAL']
        # Variables de control para mover y alcanzar la meta
        self._goal = None # Definimos la meta
        self._idist_to_goal = 0.0
        self._iyaw_error = 0.0
        self._base_ang_vel = base_ang_vel
        self._base_lin_vel = base_lin_vel
        self._min_dist_to_goal = min_dist
        self._yaw_tolerance = yaw_tolerance
        # Variables para publicador y susbscriptor
        self._cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self._odometry_sub = rospy.Subscriber('/odom', Odometry, self._on_odometry_update)
        # Implementacion de actionlib
        self._feedback = RobotMoveMsg_Feedback()
        # Declaramos el servidor en una variable de clase
        self._server = actionlib.SimpleActionServer('Robot_Move_Server', RobotMoveMsg_Action, self._execute, False)
        

    def _on_odometry_update(self,odom_msg):
        pass

    ########################################
    ## Metodos para el moviento del robot ##
    ########################################


    ####################################################
    ## Metodos para el control del flujo de Actionlib ##
    ####################################################
    def _execute (self,goal):
        success = True # Es una variable global para saber si es exitoso
        rospy.loginfo('Recibi una meta!!!')
        # Validamos la nueva GOAL
        if not self._accept_goal(goal):
            rospy.logerr('NEW GOAL rechazada, el robot esta en el estado \'%s\'.',self._code_states[self._state_code])
            self._server.set_aborted()
            return
        rospy.loginfo("NEW GOAL aceptada, dirigiendome a (%s,%s) con estado '%s'", self._goal.point.x, self._goal.point.y, self._code_states[self._state_code])

    def _accept_goal(self,goal):
        if self._state_code == 0 or self._state_code == 3:
            self._state_code == 2 # Dejamos al robot en el estado inicial para comenzar a hacer las cosas
            self._goal = goal.target
            return True
        rospy.logwarn('GOAL rechazada.')
        return False


def main():
    pass

if __name__=='__main__':
    main()