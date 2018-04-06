#2011003241
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = np.radians(0)

debug = True

def drawFrame():
    global debug
    if not debug:
        return
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex3fv(np.array([.0,.0,.0]))
    glVertex3fv(np.array([1.,.0,.0]))
    glColor3ub(0,255,0)
    glVertex3fv(np.array([.0,.0,.0]))
    glVertex3fv(np.array([.0,1.,.0]))
    glColor3ub(0,0,255)
    glVertex3fv(np.array([.0,.0,.0]))
    glVertex3fv(np.array([.0,.0,1.]))
    glEnd()

def drawCube():
    glBegin(GL_QUADS)
    glVertex3f(1.0, 1.0,-1.0) 
    glVertex3f(-1.0, 1.0,-1.0) 
    glVertex3f(-1.0, 1.0, 1.0) 
    glVertex3f(1.0, 1.0, 1.0)

    glVertex3f(1.0,-1.0, 1.0) 
    glVertex3f(-1.0,-1.0, 1.0) 
    glVertex3f(-1.0,-1.0,-1.0) 
    glVertex3f(1.0,-1.0,-1.0)

    glVertex3f(1.0, 1.0, 1.0) 
    glVertex3f(-1.0, 1.0, 1.0) 
    glVertex3f(-1.0,-1.0, 1.0) 
    glVertex3f(1.0,-1.0, 1.0)
    
    glVertex3f(1.0,-1.0,-1.0) 
    glVertex3f(-1.0,-1.0,-1.0) 
    glVertex3f(-1.0, 1.0,-1.0) 
    glVertex3f(1.0, 1.0,-1.0)

    glVertex3f(-1.0, 1.0, 1.0) 
    glVertex3f(-1.0, 1.0,-1.0) 
    glVertex3f(-1.0,-1.0,-1.0) 
    glVertex3f(-1.0,-1.0, 1.0)

    glVertex3f(1.0, 1.0,-1.0) 
    glVertex3f(1.0, 1.0, 1.0) 
    glVertex3f(1.0,-1.0, 1.0) 
    glVertex3f(1.0,-1.0,-1.0) 
    glEnd()

# draw a sphere of radius 1, centered at the origin.
# # numLats: number of latitude segments (horizontal)
# numLongs: number of longitude segments (horizontal)
def drawSphere(numLats=12, numLongs=12): 
    for i in range(0, numLats + 1): 
        lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats))) 
        z0 = np.sin(lat0) 
        zr0 = np.cos(lat0)

        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats))) 
        z1 = np.sin(lat1) 
        zr1 = np.cos(lat1)

        # Use Quad strips to draw the sphere
        glBegin(GL_QUAD_STRIP)
        for j in range(0, numLongs + 1): 
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng) 
            y = np.sin(lng) 
            glVertex3f(x * zr0, y * zr0, z0) 
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

def drawBox():
    glBegin(GL_QUADS)
    glVertex3fv(np.array([1,1,0.]))
    glVertex3fv(np.array([-1,1,0.]))
    glVertex3fv(np.array([-1,-1,0.]))
    glVertex3fv(np.array([1,-1,0.]))
    glEnd()

def drawJoint(length):
    glPushMatrix()

    glTranslatef(0,0.25,0)
    glScalef(1,0.1,1)
    drawSphere()

    glPopMatrix()


def addFinger(pos,length):
    glPushMatrix()

    glTranslatef(pos[0],pos[1],pos[2])
    glScalef(.125,.125,.125)
    
    glPushMatrix()

    glRotatef(45,1,0,0)
    glTranslatef(0,.5,0)
    
    glColor3ub(255,0,0)
    drawSphere()

    glPushMatrix()

    glTranslatef(0,2,0)
    glPushMatrix()

    glScale(1,length*10,1)
    glColor3ub(255,255,0)
    drawCube()

    glPopMatrix()

    """
    glPushMatrix()

    glRotatef(45,1,0,0)
    glTranslatef(0,.5,0)
    
    glColor3ub(255,0,0)
    drawSphere()

    glPushMatrix()

    glTranslatef(0,2,0)
    glPushMatrix()

    glScale(1,length*10,1)
    glColor3ub(255,255,0)
    drawCube()

    glPopMatrix()

    glPopMatrix()

    glPopMatrix()
    """

    glPopMatrix()

    glPopMatrix()

    glPopMatrix()

def render(camAng,count):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()
    glOrtho(-1,1,-1,1,-10,10)
    gluLookAt(1 * np.sin(camAng),1,1 * np.cos(camAng),0,0,0,0,1,0)    

    drawFrame()

    glPushMatrix()
   
    #center
    glTranslate(0,-0.5,0)
    glPushMatrix()
    
    glScalef(0.5,0.5,.1)
    glColor3ub(255,255,255)
    drawCube()

    #remove scale
    glPopMatrix()
    
    #manually scaled position
    #pinky
    addFinger(np.array([-.375,.5,0]),.3)
    #ring
    addFinger(np.array([-.125,.5,0]),.4)
    #middle
    addFinger(np.array([.125,.5,0]),.5)
    #index
    addFinger(np.array([.375,.5,0]),.4)

    glPopMatrix()


def key_callback(window,key,scancode,action,mods):
    global gCamAng

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_1:
            gCamAng+=np.radians(-10)
        elif key == glfw.KEY_3:
            gCamAng +=np.radians(10)

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2011003241",None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window,key_callback)
    glfw.swap_interval(1)

    count = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gCamAng,count)
        glfw.swap_buffers(window)
        count+=1

    glfw.terminate()

if __name__ == "__main__":
    main()