

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import argparse
#pygame: Used for creating the game window and handling events.
# OpenGL.GL and OpenGL.GLU: Used for rendering graphics using OpenGL.
# argparse: For handling command-line arguments to toggle fullscreen mode.

# Argument parser to toggle fullscreen mode
parser = argparse.ArgumentParser(description='Train animation in OpenGL with Pygame')
# ArgumentParser is a class within the argparse module that is used to handle command-line arguments
parser.add_argument('--fullscreen', action='store_true', help='Enable fullscreen mode')
# add_argument is a method of the ArgumentParser object that defines what command-line options the program is expecting.
# action='store_true' specifies that if the --fullscreen argument is present on the command line, 
args = parser.parse_args()

pygame.init()

# Check if fullscreen mode is enabled
if args.fullscreen:
    display = pygame.display.set_mode((0, 0), DOUBLEBUF | OPENGL | FULLSCREEN)
    fullscreen = True
# DOUBLEBUF: Enables double buffering, which helps reduce flickering by rendering graphics in an off-screen buffer before copying them to the display.
# OPENGL: Initializes an OpenGL context, allowing the program to use OpenGL for rendering.
else:
    display = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL | RESIZABLE)
    fullscreen = False
# pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL | RESIZABLE) sets the display mode to a window with a resolution of 800x600 pixels.
# RESIZABLE allows the window to be resized by the user.
# fullscreen = False sets a variable to indicate that the display is not in fullscreen mode.

width, height = pygame.display.get_surface().get_size()
gluOrtho2D(0, width, 0, height)

def resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    # The projection matrix defines the properties of the camera that views the objects in the world, such as the field of view, aspect ratio, and near and far clipping planes.
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    # This defines a 2D orthographic (parallel) projection matrix, which maps the specified rectangular region of the world coordinates to the viewport. Here, it maps the coordinates (0, 0) to (width, height) of the window. This means that the coordinate (0,0) will be at the lower-left corner of the window, and (width, height) will be at the upper-right corner of the window.
    glMatrixMode(GL_MODELVIEW)
    # This switches the current matrix mode to the model-view matrix. The model-view matrix is used to transform the vertices of your objects from world space to camera space.
    glLoadIdentity()

def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def plot_circle_points(h, k, x, y, filled=False):
    points = [(x + h, y + k), (-x + h, y + k), (x + h, -y + k), (-x + h, -y + k),
              (y + h, x + k), (-y + h, x + k), (y + h, -x + k), (-y + h, -x + k)]
    if filled:
        for i in range(-x, x+1):
            draw_pixel(h + i, k + y)
            draw_pixel(h + i, k - y)
        for i in range(-y, y+1):
            draw_pixel(h + i, k + x)
            draw_pixel(h + i, k - x)
    else:
        for point in points:
            draw_pixel(*point)

def draw_circle(h, k, r, filled=False):
    d = 1 - r
    # d is the decision variable. It determines whether the next point will be (x+1, y) or (x+1, y-1).
    x = 0
    y = r
    while y > x:
        plot_circle_points(h, k, x, y, filled)
        if d < 0:
            # (x+1,y)
            d += 2 * x + 3
        else:
            # (x+1,y-1)
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
    plot_circle_points(h, k, x, y, filled)

def draw_cloud(x, y):
    # The draw_cloud function creates a cloud by drawing multiple overlapping filled circles
    glColor3f(1.0, 1.0, 1.0)  # White color
    draw_circle(x, y, 20, filled=True)
    draw_circle(x + 20, y + 10, 20, filled=True)
    draw_circle(x + 40, y, 20, filled=True)
    draw_circle(x + 30, y - 15, 20, filled=True)
    draw_circle(x + 10, y - 15, 20, filled=True)

def draw_tree(x, y):
    # Draw the tree trunk
    glColor3f(0.545, 0.271, 0.075)  # Brown
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x, y + 40)
    glVertex2f(x + 20, y + 40)
    glVertex2f(x + 20, y)
    glEnd()

    # Draw the tree leaves
    glColor3f(0.0, 0.5, 0.0)  # Green
    draw_circle(x + 10, y + 60, 30, filled=True)
    draw_circle(x + 10, y + 90, 25, filled=True)
    draw_circle(x + 10, y + 115, 20, filled=True)

def draw_train(x):
    # Draw sky
    glColor3f(0.529, 0.808, 0.922)  # Light blue
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(0, height)
    glVertex2f(width, height)
    glVertex2f(width, 0)
    glEnd()
    # glVertex2f(x, y) defines a vertex of the quadrilateral:
# glVertex2f(0, 0) specifies the bottom-left corner of the quadrilateral.
# glVertex2f(0, height) specifies the top-left corner.
# glVertex2f(width, height) specifies the top-right corner.
# glVertex2f(width, 0) specifies the bottom-right corner.

    # Draw clouds
    draw_cloud(150, 500)
    draw_cloud(300, 550)
    draw_cloud(500, 520)
    draw_cloud(650, 540)
    draw_cloud(800, 500)   # Additional cloud
    draw_cloud(950, 530)   # Additional cloud
    draw_cloud(1100, 510)  # Additional cloud
    draw_cloud(1250, 550)  # Additional cloud
    draw_cloud(1400, 530)  # Additional cloud

    # Draw ground
    glColor3f(0.0, 0.502, 0.0)  # Green
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(0, 100)
    glVertex2f(width, 100)
    glVertex2f(width, 0)
    glEnd()

    # Draw houses and trees
    draw_house(100, 100)
    draw_tree(200, 100)
    draw_house(300, 100)
    draw_tree(400, 100)
    draw_house(500, 100)
    draw_tree(600, 100)
    draw_house(700, 100)
    draw_tree(800, 100)
    draw_house(900, 100)
    draw_tree(1000, 100)
    draw_house(1100, 100)
    draw_tree(1200, 100)
    draw_house(1300, 100)
    draw_tree(1400, 100)

    # Draw horizontal ladder (railway tracks) below the wheels
    glColor3f(0.545, 0.271, 0.075)  # Brown
    glLineWidth(4.0)  # Thicken the lines
    # Vertical sides of the ladder
    glBegin(GL_LINES)
    glVertex2f(0, 35)
    glVertex2f(width, 35)
    glVertex2f(0, 65)
    glVertex2f(width, 65)
    glEnd()
    # Horizontal rungs of the ladder
    for i in range(0, width+1, 40):  # Spacing rungs every 40 units
        glBegin(GL_LINES)
        glVertex2f(i, 35)
        glVertex2f(i, 65)
        glEnd()

    # Draw train
    glBegin(GL_POLYGON)  # Engine
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x, 50)
    glVertex2f(x + 165, 50)
    glVertex2f(x + 165, 150)
    glVertex2f(x + 25, 150)
    glVertex2f(x, 100)
    glEnd()

    glBegin(GL_POLYGON)  # Coach 1
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x + 175, 50)
    glVertex2f(x + 282, 50)
    glVertex2f(x + 282, 150)
    glVertex2f(x + 175, 150)
    glEnd()

    glBegin(GL_POLYGON)  # Coach 2
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x + 293, 50)
    glVertex2f(x + 400, 50)
    glVertex2f(x + 400, 150)
    glVertex2f(x + 293, 150)
    glEnd()

    glBegin(GL_POLYGON)  # Coach 3
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x + 411, 50)
    glVertex2f(x + 518, 50)
    glVertex2f(x + 518, 150)
    glVertex2f(x + 411, 150)
    glEnd()

    # Draw windows on the Engine
    glColor3f(1.0, 1.0, 0.0)  # Yellow color
    glBegin(GL_QUADS)
    glVertex2f(x + 30, 100)
    glVertex2f(x + 30, 130)
    glVertex2f(x + 60, 130)
    glVertex2f(x + 60, 100)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(x + 70, 100)
    glVertex2f(x + 70, 130)
    glVertex2f(x + 100, 130)
    glVertex2f(x + 100, 100)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(x + 110, 100)
    glVertex2f(x + 110, 130)
    glVertex2f(x + 140, 130)
    glVertex2f(x + 140, 100)
    glEnd()

    # Draw windows on Coach 1
    glBegin(GL_QUADS)
    glVertex2f(x + 185, 100)
    glVertex2f(x + 185, 130)
    glVertex2f(x + 215, 130)
    glVertex2f(x + 215, 100)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(x + 225, 100)
    glVertex2f(x + 225, 130)
    glVertex2f(x + 255, 130)
    glVertex2f(x + 255, 100)
    glEnd()

    # Removed third window from Coach 1
    # Draw windows on Coach 2
    glBegin(GL_QUADS)
    glVertex2f(x + 305, 100)
    glVertex2f(x + 305, 130)
    glVertex2f(x + 335, 130)
    glVertex2f(x + 335, 100)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(x + 345, 100)
    glVertex2f(x + 345, 130)
    glVertex2f(x + 375, 130)
    glVertex2f(x + 375, 100)
    glEnd()

    # Removed third window from Coach 2

    # Draw windows on Coach 3
    glBegin(GL_QUADS)
    glVertex2f(x + 421, 100)
    glVertex2f(x + 421, 130)
    glVertex2f(x + 451, 130)
    glVertex2f(x + 451, 100)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(x + 461, 100)
    glVertex2f(x + 461, 130)
    glVertex2f(x + 491, 130)
    glVertex2f(x + 491, 100)
    glEnd()

    # Draw wheels
    draw_circle(x + 25, 50, 15)
    draw_circle(x + 82, 50, 15)
    draw_circle(x + 140, 50, 15)
    draw_circle(x + 210, 50, 15)
    draw_circle(x + 250, 50, 15)
    draw_circle(x + 335, 50, 15)
    draw_circle(x + 375, 50, 15)
    draw_circle(x + 455, 50, 15)
    draw_circle(x + 495, 50, 15)

def draw_house(x, y):
    # Draw the house base
    glColor3f(0.0, 0.0, 1.0)  # Blue color
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x, y + 100)
    glVertex2f(x + 100, y + 100)
    glVertex2f(x + 100, y)
    glEnd()

    # Draw the house roof
    glColor3f(0.545, 0.271, 0.075)  # Brown color
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y + 100)
    glVertex2f(x + 50, y + 150)
    glVertex2f(x + 100, y + 100)
    glEnd()

    # Draw the door
    draw_door(x + 40, y)

    # Draw windows
    draw_window(x + 10, y + 50)
    draw_window(x + 65, y + 50)

def draw_door(x, y):
    glColor3f(0.647, 0.165, 0.165)  # Brown color for the door
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x, y + 50)
    glVertex2f(x + 20, y + 50)
    glVertex2f(x + 20, y)
    glEnd()

def draw_window(x, y):
    glColor3f(0.6, 0.8, 0.9)  # White color for the windows
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x, y + 20)
    glVertex2f(x + 20, y + 20)
    glVertex2f(x + 20, y)
    glEnd()

def draw_filled_circle(h, k, r):
    glColor3f(1.0, 1.0, 0.0)  # Yellow color
    draw_circle(h, k, r, filled=True)

def main():
    global fullscreen, width, height

    x = height  # Start the train from the right edge of the screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == VIDEORESIZE:
                width, height = event.size
                resize(width, height)
            elif event.type == KEYDOWN:
                if event.key == K_f:  # Press 'f' to toggle fullscreen
                    fullscreen = not fullscreen
                    if fullscreen:
                        display = pygame.display.set_mode((0, 0), DOUBLEBUF | OPENGL | FULLSCREEN)
                    else:
                        display = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL | RESIZABLE)
                    width, height = pygame.display.get_surface().get_size()
                    resize(width, height)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_train(x)
        draw_filled_circle(50, height - 50, 50)  # Drawing a filled yellow circle in the top left corner
        x-= 5.9  # Move the train to the left faster
        #5.9

        # If the train moves off the left edge, reset it to the right edge
        if x< -400:  # Assuming the length of the train is about 400 units
            x = width#width

        pygame.display.flip()
        #Purpose: Updates the display surface to show the latest rendered frame.
        pygame.time.wait(10)
        #Purpose: Pauses for 10 milliseconds between frames to control the speed of the animation.

if __name__ == "__main__":
    main()






