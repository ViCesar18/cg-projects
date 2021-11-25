import pygame as pg
from OpenGL.GL import *
import math


class App():
    def __init__(self):
        #initialise pygame
        pg.init()
        pg.display.set_mode((1280, 720), pg.OPENGL|pg.DOUBLEBUF)
        pg.display.set_caption('Brazil Flag')

        #initialise opengl
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(0, 1, 0, 1, -1, 1)

        self.mainLoop()
    

    def mainLoop(self):
        running = True
        while running:
            #check events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            
            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # draw background (green)
            vertices = [
                (0, 0, 0),
                (0, 1, 0),
                (1, 1, 0),
                (1, 0, 0)
            ]
            color = (0, 0.67, 0.35)
            draw().rectangle(vertices, color)

            # yellow rectangle
            vertices = [
                (0.5, 0.05, 0),
                (0.95, 0.5, 0),
                (0.5, 0.95, 0),
                (0.05, 0.5, 0)
            ]
            color = (0.96, 0.90, 0.09)
            draw().rectangle(vertices, color)

            # draw blue circle
            center = (0.5, 0.5)
            r = 0.20
            color = (0.16, 0.02, 0.63)
            draw().circle(center, r, color)

            pg.display.flip()

        self.quit()   


    def quit(self):
        pg.quit()


class draw():
    def rectangle(self, vertices, color):
        glColor3f(*color)
        glBegin(GL_POLYGON)

        for vertex in vertices:
            glVertex3f(vertex[0], vertex[1], vertex[2])

        glEnd()
        glFlush()

    
    def circle(self, center, r, color):
        glColor3f(*color)
        glBegin(GL_POLYGON)

        for i in range(360):
            theta = i * math.pi / 180
            glVertex3f(center[0] + r * math.cos(theta), center[1] + r * math.sin(theta), 1)
        
        glEnd()
        glFlush()


myApp = App()