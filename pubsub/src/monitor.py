#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from pubsub.msg import Estatus

def process_msg_callback(msg):
    dx = round(msg.twist.twist.linear.x,2) #se entra desde el osometry para ver las variables
    # Debido a que nuestro robot es (2,0) no puede moverse sobre el eje Y
    #dy = msg.twist.twist.linear.y #rosmsg info nav_msgs/Odometry
    theta = round(msg.twist.twist.angular.z,2)
    rospy.loginfo('Actualmente el robot tiene dx = {:.2f} m/s, tehta = {:.2f} radianes'.format(dx,theta))
    if dx == 0.0 and theta== 0.0:
        pubmsg.codigo = 0
        pubmsgestado='Detenido'
    elif dx!= 0.0 and theta == 0.0:
        pubmsg.codigo = 100
        pubmsg.estado='Solo vel lineal: {} m'.format(dx)
    elif dx!= 0.0 and theta == 0.0:
        pubmsg.codigo = 200
        pubmsg.estado='Solo vel angular: {} rad'.format(theta)
    elif dx!= 0.0 and theta == 0.0:
        pubmsg.codigo = 300
        pubmsg.estado='movimiento lineal: {} m y angular: {} rads'.format(dx,theta)
    elif dx!= 0.0 and theta == 0.0:
        pubmsg.codigo = 1000
        pubmsg.estado = 'Error'

    pub.publish(pubmsg)
    #rospy.spin()

rospy.init_node('monitor')
sub = rospy.Subscriber('odom', Odometry, process_msg_callback)
pub = rospy.Publisher('etatus', Estatus, queue_size=2)
rate = rospy.Rate(2)
pubmsg = Estatus()
rospy.spin() #Mantendremos esto vivo hasta que le demos ctrl + c

#if __name__ == "__main__":
#    init_monitor()