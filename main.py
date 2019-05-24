from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from utils import *
import math
import serial
import os
import threading
import sympy as sp
import numpy as np
import random
 
ESCAPE = '\033'
 
window = 0
 
#rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0
 
DIRECTION = 1
 

def IsSide(edge1, edge2):
    if(edge1.x1 == edge2.x1 and edge1.y1 == edge2.y1 and edge1.z1 == edge2.z1): return True
    if(edge1.x1 == edge2.x2 and edge1.y1 == edge2.y2 and edge1.z2 == edge2.z2): return True
    if(edge1.x2 == edge2.x1 and edge1.y2 == edge2.y1 and edge1.z2 == edge2.z1): return True
    if(edge1.x2 == edge2.x2 and edge1.y2 == edge2.y2 and edge1.z2 == edge2.z2): return True
    return False
 
def InitGL(Width, Height): 
 
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0) 
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)   
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
 
def keyPressed(*args):
        if args[0] == ESCAPE:
                sys.exit()

def GetCombineEdge(color, fromX, toX, fromY, toY, fromZ, toZ, size ):
    answer = []
    if fromY == toY:
        while fromZ < toZ - size:
                currentX = fromX
                while currentX < toX - size:
                        points = []
                        points += [Point(currentX,fromY,fromZ)]
                        points += [Point(currentX + size,fromY,fromZ)]
                        points += [Point(currentX + size ,toY,fromZ + size)]
                        points += [Point(currentX,toY,fromZ + size)]
                        answer += [SubSquare(points)]
                        currentX += size
                fromZ += size
    elif fromX == toX:
            while fromZ < toZ - size:
                currentY = fromY
                while currentY < toY - size:
                        points = []
                        color -= 0.0025
                        points += [Point(fromX,currentY,fromZ)]
                        points += [Point(fromX,currentY + size,fromZ)]
                        points += [Point(toX, currentY + size,fromZ + size)]
                        points += [Point(toX,currentY, fromZ + size)]
                        answer += [SubSquare(points)]
                        currentY += size
                fromZ += size
    else:
        while fromX < toX - size:
                currentY = fromY
                while currentY < toY - size:
                        points = []
                        points += [Point(fromX,currentY,fromZ)]
                        points += [Point(fromX,currentY + size,fromZ)]
                        points += [Point(fromX + size, currentY + size, toZ)]
                        points += [Point(fromX + size, currentY, toZ)]
                        answer += [SubSquare(points)]
                        currentY += size
                fromX += size
    return answer
 
def VectMul(point1, point2):
        return math.sqrt( (point2.x - point1.x) * (point2.x - point1.x)
         + (point2.y - point1.y) * (point2.y - point1.y)
          + (point2.z - point1.z) * (point2.z - point1.z))
 
def DrawGLScene():
        global i
        global X_AXIS,Y_AXIS,Z_AXIS
        global DIRECTION
        global E
 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 
        glLoadIdentity()
        glTranslatef(0.0,0.0,-6.0)
        glRotatef(X_AXIS,1.0,0.0,0.0)
        glRotatef(Y_AXIS,0.0,1.0,0.0)
        glRotatef(Z_AXIS,0.0,0.0,1.0)

        currentColor = 1
        diffColor = 0.15

        
        currentColor -= diffColor
        """
        glBegin(GL_QUADS)

        glColor3d(currentColor, currentColor, currentColor)
        glVertex3d(-1, 0, 1)
        glVertex3d(1, 0, 1)
        glVertex3d(1,1,1)
        glVertex3d(-1,1,1)

        currentColor -= diffColor
        glColor3d(currentColor, currentColor, currentColor)
        glVertex3d(-1, 1, 1)
        glVertex3d(-1, 1, -1)
        glVertex3d(1,1,-1)
        glVertex3d(1,1,1)

        currentColor -= diffColor
        glColor3d(currentColor, currentColor, currentColor)
        glVertex3d(-1, 1, -1)
        glVertex3d(1, 1, -1)
        glVertex3d(1,0,-1)
        glVertex3d(-1,0,-1)

        currentColor -= diffColor
        glColor3d(currentColor, currentColor, currentColor)
        glVertex3d(1, 1, 1)
        glVertex3d(1, 1, -1)
        glVertex3d(1,0,-1)
        glVertex3d(1,0,1)
        currentColor -= diffColor

        glColor3d(currentColor, currentColor, currentColor)
        glVertex3d(-1, 1, 1)
        glVertex3d(-1, 1, -1)
        glVertex3d(-1,0,-1)
        glVertex3d(-1,0,1)
        currentColor -= diffColor
 
        glEnd()
        """
        power = 100
        point = Point(2, 2, 2)
        global combineEdges
        for edge in combineEdges:
                print(edge.visible, "ogogo")
                for subSquare in edge.subSquares:
                        subSquare.Draw()#random.randrange(0, 100, 1)/100.0)
        
        glBegin(GL_LINES)

        glColor3d(255, 0, 0)
        glVertex3d(-1 - 0.01, 1, 1 + 0.0)
        glVertex3d(-1 - 0.01, 1, -1 - 0.01)

        glVertex3d(-5, 5, 5)
        glVertex3d(8, 8, 8)

        

        glEnd()
 

        glBegin(GL_LINES);
        glColor3d(1,0,0);     
        glVertex3d(-4.5,3,0);
        glVertex3d(-3,3,0);
        glColor3d(0,1,0);  
        glVertex3d(-3,3.3,0);
        glVertex3d(-4,3.4,0);
        glEnd();

        glPointSize(10)

        glBegin(GL_POINTS)
        glColor3d(1, 0, 0)
        glVertex3d(light.x, light.y, light.z)
        glEnd()
 
        X_AXIS = X_AXIS - 0.30
        Z_AXIS = Z_AXIS - 0.30
 
        glutSwapBuffers()


def IsOnSide(edge, normal):
    return (np.array([edge.x1, edge.y1, edge.z1, 1]).dot(normal.T) == 0 and 
    (np.array([edge.x2, edge.y2, edge.z2, 1]).dot(normal.T)) == 0)


def GetNormalVector(edge1, edge2):
    x, y, z = sp.symbols('x, y, z')
    mx = np.array([[x - edge1.x1, edge1.x2 - edge1.x1, edge2.x2 - edge1.x1],
        [y - edge1.y1, edge1.y2 - edge1.y1, edge2.y2 - edge1.y1],
        [z - edge1.z1, edge1.z2 - edge1.z1, edge2.z2 - edge1.z1]])
    poly = sp.Matrix(mx).det()
    normal = [0, 0, 0, 0]
    normal[3] = poly.subs(x, 0).subs(y, 0).subs(z, 0)
    normal[0] = poly.subs(x, 1).subs(y, 0).subs(z, 0) - normal[3]
    normal[1] = poly.subs(x, 0).subs(y, 1).subs(z, 0) - normal[3]
    normal[2] = poly.subs(x, 0).subs(y, 0).subs(z, 1) - normal[3]
    return normal

def RemoveDuplicates(normals):
    i = 0
    while i < len(normals):
        j = 0
        while j < len(normals):
            if(i != j):
                if (((normals[i][0] == normals[j][0] and normals[i][1] == normals[j][1]
                and normals[i][2] == normals[j][2] and normals[i][3] == normals[j][3])) 
                or 
                ((-normals[i][0] == normals[j][0] and -normals[i][1] == normals[j][1]
                and -normals[i][2] == normals[j][2] and -normals[i][3] == normals[j][3]))):
                    normals.remove(normals[j])
            j = j + 1
        i = i + 1

def GetUniquePoints(edges):
    points = list()
    for e in edges:
        if(not [e.x1, e.y1, e.z1] in points):
            points.append([e.x1, e.y1, e.z1])
        if(not [e.x2, e.y2, e.z2] in points):
            points.append([e.x2, e.y2, e.z2])
    return points


def GetCenter(edges):
    center = [0, 0, 0, 1]
    points = GetUniquePoints(edges)
    for p in points:
        for i in range(3):
            center[i] += p[i]
    for i in range(3):
        center[i] /= len(points)
    return center

def IsVisible(edge, side):
    global light
    return light.dot(side) < 0


def HideEdges(edges):
        global combineEdges
        for e in edges:
            e.visible = False
        x, y, z = sp.symbols('x, y, z')
        center  = np.array(GetCenter(edges))
        normals = list()
        for e1 in edges :
            for e2 in edges:
                if(IsSide(e1, e2)):
                    normal = GetNormalVector(e1, e2)
                    if(not (normal in normals)):
                        normals.insert(len(normals), normal)
        normals.remove([0, 0, 0, 0])
        RemoveDuplicates(normals)
        for n in normals:
            print(n[0], n[1], n[2], n[3])

        body = np.array(normals).T
        print("body", body)
        print("dot", center.dot(body))
        for col in body.T:
            if (center.dot(col.T)) < 0:
                for i in range(len(col)):
                    col[i] *= -1
        print("body2", body)
        print("dot", center.dot(body))
        for side in body.T:
            
            print("SIDE", IsVisible(light, side))
            if(IsVisible(light, side)):
                for e in edges:
                    if IsOnSide(e, side):
                        e.visible = True
                        pass
            combineEdges[i].visible = IsVisible(light, side)
        print(body.T[0])
        print("E", light.dot(body.T[0]))



def main():
 
        global window
        global i
        global combineEdges
        global light
        global power
        power = 4
        light = Point(1.5, 1, 2)
        combineEdges = [0, 0, 0, 0, 0, 0]

        combineEdges[0] = CombineEdge(1, -1, 1, 0, 0, -1, 1, 0.1)
        combineEdges[1] = CombineEdge(1, -1, 1, 1, 1, -1, 1, 0.1)
        combineEdges[2] = CombineEdge(1, 1, 1, 0, 1, -1, 1, 0.1)
        combineEdges[3] = CombineEdge(1, -1, -1, 0, 1, -1, 1, 0.1)
        combineEdges[4] = CombineEdge(1, -1, 1, 0, 1, 1, 1, 0.1)
        combineEdges[5] = CombineEdge(1, -1, 1, 0, 1, -1, -1, 0.1)
        input()
        for edge in combineEdges:
                for subSquare in edge.subSquares:
                        color = (power - VectMul(subSquare.points[0], light))/power
                        if color <= 0.1:
                                color = 0.1
                        subSquare.color = color
        edgesOfedges = [] #hm...
        for edge in combineEdges:
                edgesOfedges += edge.edges
        HideEdges(edgesOfedges)
        input()
        
        
        for edge in combineEdges:
                for edgeEdge in edge.edges:
                        print(edgeEdge.visible)
                        if not edgeEdge.visible: edge.visible = False
                print("")
        

        for edge in combineEdges:
                print(edge.visible, "aga")
                for subSquare in edge.subSquares:
                        color = (power - VectMul(subSquare.points[0], light))/power
                        if color <= 0.1 or not edge.visible:
                                color = 0.1
                        subSquare.color = color

 
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640,480)
        glutInitWindowPosition(200,200)

        window = glutCreateWindow('OpenGL Python Cube')
 
        glutDisplayFunc(DrawGLScene)
        glutIdleFunc(DrawGLScene)
        glutKeyboardFunc(keyPressed)
        InitGL(640, 480)
        glutMainLoop()
 
if __name__ == "__main__":
        main() 
