#!/usr/bin/env python

import rospy
import math
from rospy.core import deprecated, rospydebug
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point

class MovementDetector(object):
    # Declaramos la clase con un constructor
    def __init__(self):
        """Inicializamos los valores de la clase"""
        self._mved_distance = Float64() # Este es un objeto
        self._mved_distance.data = 0.0 # Este es el valor del objeto
        self._current_position = Point()# Es uno de los tipos de mensje que se utulizan en ros
        self.get_init_position()
        self.distance_mved_pub = rospy.Publisher('/moved_distance', Float64, queue_size=1)
        self.distance_mved_sub = rospy.Subscriber('odom', Odometry,self.odom_callback)

# Necesitamos una función para poder calcular todo lo que tnemeos

def get_init_position(self):
    data_odom = None #Función de espera
    while data_odom is None:
        try:
            #Encerramos este codigo en un siclo de espera
            data_odom = rospy.wait_for_message('/odom',Odometry,timeout=1)
        except Exception as e:
            # Muy usada para depurar print (str(e))
            rospy.logerr(e)
            # rospy.loginfo("El topico no se encuentra activo, esperando.")
    # Si salimos del ciclo, quiere decir que la variable ya esta inicializada
    self._current_position.x = data_odom.pose.pose.position.x
    self._current_position.y = data_odom.pose.pose.position.y
    self._current_position.z = data_odom.pose.pose.position.z

def odom_callback(self,msg):
    NewPos = msg.pose.pose.postion
    self._mved_distance.data += self.calculate_distance(NewPos,self._current_position)
    self.update_curpos(NewPos)
    if self._mved_distance.data<0.000001:
        aux = Float64()
        aux.data = 0.0
        self.distnace_moved_pub.publish(aux)
    else:
        self.distance_moved_pub.piblish(self._mved_distance)

def update_curpos(self,newpos):
    self._current_position.x = newpos.x
    self._current_position.x = newpos.y
    self._current_position.x = newpos.z

def calculate_distance(self,NewPos,CurPos):
    x2=NewPos.x
    x1=CurPos.x
    y2=NewPos.y
    y1=CurPos.y

    dist =math.hypot(x2-x1,y2-y1)
    return dist

def publish_moved_distance(self):
    # spin() simplemente evita que Python salga hasta que el nodo se detenga
    rospy.spin()


if __name__ =='__main__':
    # Crear un nodo para correr el proceso
    rospy.init_node('movement_detector_node')
    # Creamos la instancia de la clase MovementDetector y poner el programa a funcionar
    mov_det = MovementDetector()
    mov_det = publish_moved_distance