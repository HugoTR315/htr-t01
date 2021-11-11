#!/usr/bin/env python

import rospy
from gazebo_msgs.srv import GetWorldProperties, GetModelState

class GazaboUtils(object):
    def __init__(self) -> None:
        pass
    def getWorldProperties(self):
        try:
            get_world_properties=rospy.ServiceProxy('/gazebo/get_world_properties',GetWorldProperties)
            wp=get_world_properties()
            if wp.success:
                return wp
            else:
                rospy.logwarn(wp.status_message)
                return None
        except rospy.ServiceException as e:
            rospy.logerr('Al llamar /gazebo/get_world_properties: %s'%e)

    def getModelState(self,model_name,relative_entity_name='world'):
        try:
            get_model_state=rospy.ServiceProxy('/gazebo/get_model_state',GetModelState)
            ms=get_model_state(model_name,relative_entity_name)
            if ms.success:
                return ms
            else:
                rospy.logwarn(ms.status_messages)

        except rospy.ServiceException as e:
            rospy.logerr('Al llamar /gazebo/get_model_state: %s'%e)
    
    def get_model_Pose(self,model_name):
        ms = self.getModelState(model_name)
        if ms:
            return ms.pose
        else:
            return None

# class DisntanceMonitor():
    





def test_services():
    gazebo_utils=GazaboUtils()
    exclude = ['ground_plane','turtlebot3_waffle']
    landmarks = {}
    print('Probando GazeboUtils, get_world_properties service:')
    wp = gazebo_utils.getWorldProperties()
    if not wp:
        for model in wp.model_names:
            if model not in exclude:
                ms=gazebo_utils.getModelState()
                if ms:
                    position = (ms.pose.position.x,ms.pose.position.y)
                    landmarks.update({model: position})
                else:
                    print('Fallo la llamada al servicio /gazebo/get_model_state')
        return landmarks
    else:
        print('Fallo la llamada al servicio /gazebo/get_world_properties')

if __name__=='__main__':
    landmarks = test_services
    if landmarks:
        print(landmarks)
    else:
        print('Falló al final')