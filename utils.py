
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def dot(self, point):
        return self.x * point[0] + self.y * point[1] + self.z * point[2]

class SubSquare(object):
    def __init__(self, points, color = 0.2):
        self.points = points
        self.color = color

    def Draw(self):
        glBegin(GL_QUADS)
        glColor3d(self.color, self.color, self.color)
        glVertex3d(self.points[0].x, self.points[0].y, self.points[0].z)
        glVertex3d(self.points[1].x, self.points[1].y, self.points[1].z)
        glVertex3d(self.points[2].x, self.points[2].y, self.points[2].z)
        glVertex3d(self.points[3].x, self.points[3].y, self.points[3].z) # x!
        glEnd()



class Edge(object):
    def __init__(self, x1, y1, z1, x2, y2, z2, visible = True):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.visible = visible

class CombineEdge(object):
    def GetCombineEdge(self, color, fromX, toX, fromY, toY, fromZ, toZ, size ):
        self.visible = True
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
    def __init__(self, color, fromX, toX, fromY, toY, fromZ, toZ, size):
        self.edges = []
        if fromX == toX:
            self.edges += [Edge(fromX, fromY, fromZ, fromX, toY, fromZ)]
            self.edges += [Edge(fromX, toY, fromZ, fromX, toY, toZ)]
            self.edges += [Edge(fromX, toY, toZ, fromX, fromY, toZ)]
            self.edges += [Edge(fromX, fromY, toZ, fromX, fromY, fromZ)]
        if fromY == toY:
            self.edges += [Edge(fromX, fromY, fromZ, toX, fromY, fromZ)]
            self.edges += [Edge(toX, fromY, fromZ, toX, fromY, toZ)]
            self.edges += [Edge(toX, fromY, toZ, fromX, fromY, toZ)]
            self.edges += [Edge(fromX, fromY, toZ, fromX, fromY, fromZ)]
        if fromZ == toZ:
            self.edges += [Edge(fromX, fromY, fromZ, fromX, toY, fromZ)]
            self.edges += [Edge(fromX, toY, fromZ, toX, toY, fromZ)]
            self.edges += [Edge(toX, toY, fromZ, toX, fromY, fromZ)]
            self.edges += [Edge(toX, fromY, fromZ, fromX, fromY, fromZ)]
        self.subSquares = self.GetCombineEdge(color, fromX, toX, fromY, toY, fromZ, toZ, size)

    



def main():
    pass

if __name__ == "__main__":
    main()