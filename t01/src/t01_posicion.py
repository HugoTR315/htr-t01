#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from pubsub.msg import Estatus


def init_monitor():
    sub = rospy.Subscriber('odom', Odometry, process_msg_callback)
    rospy.init_node('monitor')
    rospy.spin()

def process_msg_callback(msg):
    px = msg.pose.pose.position.x
    py = msg.pose.pose.position.y
    ox = msg.pose.pose.orientation.x
    oy = msg.pose.pose.orientation.y
    rospy.loginfo('Actualmente el robot tiene posicion x = {:.2f} m/s, y = {:.2f} m/s, orientacion x = {:.2f} m/s, y = {:.2f} m/s,'.format(px,py,ox,oy))

if __name__ == "__main__":
    init_monitor()