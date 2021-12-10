#! /usr/bin/env python
from _typeshed import Self
from nav_msgs import msg
import rospy
import actionlib
from actionlib import GoalStatus
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PointStamped, Point, Twist
from robot_move.msg import RobotMoveMsg_Action, RobotMoveMsg_Feedback, RobotMoveMsg_Result
from tf import transformations
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
        self._ipose.point = odom_msg.pose.pose.position
        self._ipose.header.seq = odom_msg.header.seq
        self._ipose.header.stamp = odom_msg.header.stamp
        self._ipose.header.frame_id = odom_msg.header.frame_id
        quaternion = [
            odom_msg.pose.pose.orientation.x,
            odom_msg.pose.pose.orientation.y,
            odom_msg.pose.pose.orientation.z,
            odom_msg.pose.pose.orientation.w
        ]
        euler_angles = transformations.euler_from_quaternion(quaternion)
        self._iorient_rpy.x = euler_angles[0] # roll - alfa
        self._iorient_rpy.y = euler_angles[1] # pitch - beta
        self._iorient_rpy.z = euler_angles[2] # yaw - gama


    ########################################
    ## Metodos para el moviento del robot ##
    ########################################
    def _head_towards_goal(self):
        pass

    def _go_staight (self):
        pass

    def _update_goal_vector(self):
        dx = self._goal.target.point.x - self._ipose.point.x
        dy = self._goal.target.point.y - self._ipose.point.y
        self._idist_to_goal = math.hypot(dx,dy)
        goal_yaw = math.atan2(dy,dx)
        self._iyaw_error = goal_yaw - self._iorient_rpy.z

    def _stop_robot(self):
        rospy.loginfo("Deteniendo el robot")
        stop_msg = Twist()
        stop_msg.linear.x = 0
        stop_msg.linear.y = 0
        stop_msg.linear.z = 0
        stop_msg.angular.x = 0
        stop_msg.angular.y = 0
        stop_msg.angular.z = 0
        self._cmd_vel_pub.publish(Twist())
        rospy.sleep(1)
        self._state_code = 0

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
        
        while not self._state_code == 3:
            # Tomamos una accion de acuerdo al estado de 
            # la maquina de estados de nuestro robot
            if self._server.is_preempt_requested():
                success = False
                rospy.logwarn("PREEMPT signal received!")
                break

            if self._state_code == 0:
                success == False
                rospy.logwarn("Robot detenido, esperando para reanudad")
            elif self._state_code == 1:
                self._head_towards_goal()
            elif self._state_code == 2:
                self._go_staight()
            else:
                success = False
                rospy.logerr("Assert error: No se que hago aqui, estatus (%s) '%s'",self._state_code,self._code_states[self._state_code])
                break
        self._publish_feedback()

        # Reportamos los resultados
        result = self._get_result_msg(success)
        self._stop_robot()
        if success:
            self._server.set_succeeded(result,"GOAL reached!")
        else:
            self._server.set_succeeded(result,)
            rospy.logwarn("GOAL PREEMTED")


    def _accept_goal(self,goal):
        if self._state_code == 0 or self._state_code == 3:
            self._state_code == 2 # Dejamos al robot en el estado inicial para comenzar a hacer las cosas
            self._goal = goal.target
            return True
        rospy.logwarn('GOAL rechazada.')
        return False

    def _publish_feedback(self):
        self._feedback.i_state_code = self._state_code
        self._feedback.i_state_name = self._code_states[self._state_code]
        self._feedback.i_distance_error = self._idist_to_goal
        self._feedback.i_yaw_error = self._iyaw_error
        self._server.publish_feedback(self._feedback)

    def _get_result_msg(self, success):
        result = RobotMoveMsg_Result()
        result.state_code = self._state_code
        result.state_name = self._code_states[self._state_code]
        result.distance_error = self._idist_to_goal
        result.yaw_error = self._iyaw_error
        result.sucess = False
        if success:
            result.goal_massage = "Goal complete! Posicion actual ({:.6f},{:.6f})".format(self._ipose.point.x,self._ipose.point.y)
        else:
            result.goal_massage = "Goal failed! Posicion actual ({:.6f},{:.6f})".format(self._ipose.point.x,self._ipose.point.y)
        return result

def main():
    pass

if __name__=='__main__':
    main()