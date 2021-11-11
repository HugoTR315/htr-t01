# [ROS-Simulación, Tarea 01]

| Código | Description |
| ------ | ----------- |
| Asignatura   | Temas Selectos de Mecatrónica |
| Tarea | T01 |

## Contenido

- [Objetivo](#objetivo)
- [Desarrollo](#Desarrollo)
- [Conclusiones](#Conclusiones)
- [Autor](#Autor)
- [Referencias](#Referencias)

## Objetivo

Que el alumno diseñe un programa donde modifique el comportamiento de un robot a partir de los siguientes comandos de texto:

* Avanza  [velocidad lineal]
* Gira        [velocidad angular]
* Detente

## Desarrollo

Obtener la información del cmd_vel para saber con qué mensajes estamos trabajando y de esta manera poder modificar la posición de nuestro robot a través de los comandos "gira", "avanza" y "detente".

Posteriormente creamos las variables WAFFLE_MAX_LIN_VEL, WAFFLE_MAX_ANG_VEL, LIN_VEL_STEP_SIZE y ANG_VEL_STEP_SIZE las cuales nos ayudaran a mover a cierta velocidad nuestro robot, posteriormente con las cuatro funciones que creamos, logramos obtener las velocidades necesarias para hacer que nuestro robot se mueva de forma adecuada a lo que nosotros buscamos, es decir, avanzar, girar y detenernos.

Finalmente, con ayuda de un bucle while, podemos hacer que nuestro programa nos pida siempre el comando asignado "Detente", "Avanza" o "Gira" y así mismo, con ayuda de condiciones if, asignarle los valores necesarios para que nuestro robot cambie su estado al que nosotros le hemos asignado

## Conclusiones

Podemos observar que con ayuda de un publicador podemos cambiar el estado de nuestro robot, haciendo que avance o gire, además, podemos ver la gran importancia que tiene el conocer los topicos que maneja nuestro robot ya que de lo contrario nos encontrariamos con varios problemas, por ejemplo, en nuestro caso fue el encontrar el topico correcto para poder modifivar la velocidad de nuestro robot, por lo que tuvimos que recurrir a manuales, repositorios y algunos videos sobre el tema para poder llegar a la solución que buscabamos. 

## Autor

Torres Rocha Hugo

## Referencias

* R. (2020, 20 octubre). turtlebot3/turtlebot3_teleop_key at master · ROBOTIS-GIT/turtlebot3. GitHub. Recuperado 2 de noviembre de 2021, de https://github.com/ROBOTIS-GIT/turtlebot3/blob/master/turtlebot3_teleop/nodes/turtlebot3_teleop_key

* ROS/Tutorials - ROS Wiki. (s. f.). ROS.org. Recuperado 2 de noviembre de 2021, de http://wiki.ros.org/ROS/Tutorials