#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import sys, select, os

WAFFLE_MAX_LIN_VEL = 1
WAFFLE_MAX_ANG_VEL = 2

LIN_VEL_STEP_SIZE = 0.5
ANG_VEL_STEP_SIZE = 0.5

msg = """
Controla tu robot!
---------------------------
Comandos de movimiento:
Escribe "Avanza" o "avanza" para ir hacia delante
Escribe "Detente" o "detente" para detenerte
Escribe "Gira" o "gira" para girar
Escribe "Exit" o "exit" para salir del programa
"""

e = """Fallo la comunicacion"""

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min( input, output + slop)
    elif input < output:
        output = max( input, output - slop)
    else:
        output = input

    return output

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkLinearLimitVelocity(vel):
    if turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
      vel = constrain(vel, -WAFFLE_MAX_LIN_VEL, WAFFLE_MAX_LIN_VEL)
    return vel

def checkAngularLimitVelocity(vel):
    if turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
      vel = constrain(vel, -WAFFLE_MAX_ANG_VEL, WAFFLE_MAX_ANG_VEL)
    return vel

if __name__=="__main__":
    rospy.init_node('turtlebot3_teleop')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    # Obtenemos el modelo de turtlebot (waffle)
    turtlebot3_model = rospy.get_param("model", "burger")

    # Inicializamos nuestras variables para no tener errores
    status = 0
    target_linear_vel   = 0.0
    target_angular_vel  = 0.0
    control_linear_vel  = 0.0
    control_angular_vel = 0.0

    #Comenzamos a pedir nuetras variables
    try:
        print(msg)
        print("\n\nPor favor ingresa la accion que deseas\n\n")
        while(1):
            key=input("--> ")# Aqui la función recibe nuestro string
            # Preguntamos la accion y dependiendo de eso hacemos lo que nos indica
            if key == 'Avanza' or key == "avanza" :
                target_linear_vel = checkLinearLimitVelocity(target_linear_vel + LIN_VEL_STEP_SIZE)
                status = status + 1
                print("\nEstamos avanzando a todo gas\n")
            elif key == 'Gira' or key == "gira" :
                target_angular_vel = checkAngularLimitVelocity(target_angular_vel + ANG_VEL_STEP_SIZE)
                status = status + 1
                print("\nEstamos girando como todo un drifter\n")
            elif key == 'Detente' or key == 'detente' :
                target_linear_vel   = 0.0
                control_linear_vel  = 0.0
                target_angular_vel  = 0.0
                control_angular_vel = 0.0
                print("\nEstamos detenidos, hermano cayo la ley\n")
            elif key == "Exit" or key == "exit":
                exit()
            else:
                print("\nPor favor ingresa bien las cosas\n")

            twist = Twist()

            control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
            twist.linear.x = control_linear_vel; twist.linear.y = 0.0; twist.linear.z = 0.0

            control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_angular_vel

            pub.publish(twist)

    except:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)