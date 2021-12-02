import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

dX = 0
dY = 0
dZ = -6
rotateX = 0
rotateY = 1
rotateZ = 0
rotation = 90
size = 1


def resize(width, height):
    ar = width / height

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-ar, ar, -1, 1, 2, 100) # perspectiva

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def display():
    t = glutGet(GLUT_ELAPSED_TIME) / 1000
    angle = t * rotation
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3d(1, 0, 0)

    glPushMatrix()

    glTranslated(dX, dY, dZ)
    glRotated(angle, rotateX, rotateY, rotateZ)
    
    glutSolidTeapot(size)

    glPopMatrix()

    glutSwapBuffers()


def key(key, x, y):
    global dX, dY, dZ
    global rotateX, rotateY, rotateZ, rotation
    global size

    if key == b'w':
        dY += 0.1
    elif key == b'a':
        dX -= 0.1
    elif key == b's':
        dY -= 0.1
    elif key == b'd':
        dX += 0.1
    elif key == b'e':
        dZ += 0.1
    elif key == b'q':
        dZ -= 0.1
    elif key == b'8':
        rotateX = 1
        rotateY = 0
        rotateZ = 0
        rotation = 90
    elif key == b'4':
        rotateX = 0
        rotateY = 1
        rotateZ = 0
        rotation = -90
    elif key == b'2':
        rotateX = 1
        rotateY = 0
        rotateZ = 0
        rotation = -90
    elif key == b'6':
        rotateX = 0
        rotateY = 1
        rotateZ = 0
        rotation = 90
    elif key == b'+' and size < 4:
        size += 1
    elif key == b'-' and size > 1:
        size -= 1

    glutPostRedisplay()


def idle():
    glutPostRedisplay()


glutInit(sys.argv)
glutInitWindowSize(640, 480)
glutInitWindowPosition(10, 10)
glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

glutCreateWindow("Object Rotation")   

glutReshapeFunc(resize)
glutDisplayFunc(display)
glutKeyboardFunc(key)
glutIdleFunc(idle)

glClearColor(1, 1, 1, 1)

# Iluminação
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

glEnable(GL_LIGHT0)
glEnable(GL_NORMALIZE)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_LIGHTING)

glLightfv(GL_LIGHT0, GL_AMBIENT, [0, 0, 0, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])
glLightfv(GL_LIGHT0, GL_POSITION, [2, 5, 5, 0])

glutMainLoop()
