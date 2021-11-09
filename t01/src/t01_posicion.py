#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from pubsub.msg import Estatus
    
def init_monitor():
    #sub = rospy.Subscriber('odom', Odometry, process_msg_callback)
    #rospy.init_node('monitor')
    #rospy.spin()
    data_odom = rospy.Subscriber('/odom', Odometry, process_msg_callback)
    rospy.init_node('monitor')
    rospy.spin()
    posx=data_odom.pose.pose.postion.x
    posy=data_odom.pose.pose.postion.x
    print("Esta es la posicion en X = ",posx," Esta es la posición en Y = ",posy) # Vemos si son correctos los datos
    
def process_msg_callback(msg):
    px = msg.pose.pose.position.x
    py = msg.pose.pose.position.y
    rospy.loginfo('Actualmente el robot tiene posicion x = {:.2f} m, y = {:.2f} ms'.format(px,py))
    
if __name__ == "__main__":
    init_monitor()