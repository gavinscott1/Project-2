
import pandas as pd
import time
import pygame as py
import math
import UCNanoleaf as NL
import matplotlib.image as mpimg
from PIL import Image
import numpy as np


skip = [5,4,3,2,1,0,0,1,2,3,4,5]


def drawTris(i, j, pointsDown):
    # This function determines uses the oriantation information provided by "pointsDown" to draw a triangle
    # at the specified i (column) and j (row) index.
    iteration = 1
    if pointsDown: iteration = 0

    if j < 6 and i >= 6 - j and i <= 18 + j:
        mid = [start[0] + length / 2 * i, start[1] + (length * j)]
        tri.append(Triangle(mid, pointsDown, length, 0x000000))
        py.draw.polygon(window, 0x0, tri[-1].point, 1)

    if j >= 6 and (i > iteration + (j - 6) and i < 26 - (j - 4)):
        mid = [start[0] + length / 2 * i, start[1] + (length * j)]
        tri.append(Triangle(mid, pointsDown, length, 0x000000))
        py.draw.polygon(window, 0x0, tri[-1].point, 1)


class Triangle:
    # Used to store information about the triangles used in the simulator.
    def __init__(self, mid, inverted, length, color):
        self.mid = mid
        self.inverted = inverted
        self.length = length
        self.color = color

        if inverted:
            self.point = self.__invtri__(mid, length)
        else:
            self.point = self.__tri__(mid, length)

    def __tri__(self, mid, length):
        # Calculates the three vertext points of a equalateral triangle point up
        Ax = mid[0] - length / 2
        Bx = mid[0] + length / 2
        Cx = mid[0]
        Ay = mid[1] - (math.cos(60) * length) / 2
        By = Ay
        Cy = Ay + math.cos(60) * length
        return [(Ax, Ay), (Bx, By), (Cx, Cy)]

    def __invtri__(self, mid, length):
        # Calculates the three vertext points of a equalateral triangle point down.
        Ax = mid[0] - length / 2
        Bx = mid[0] + length / 2
        Cx = mid[0]
        Ay = mid[1] + (math.cos(60) * length) / 2
        By = Ay
        Cy = Ay - math.cos(60) * length
        return [(Ax, Ay), (Bx, By), (Cx, Cy)]

    def set_color(self, color):
        self.color = color  # Get/Set functions

    def get_color(self):
        return self._color

def show(df, T = 5):
    # This function simulates what your matrix will look like when sent to the wall, allowing you to try out your
    # code even when you can't physically access the wall. One limitation of this is that transition effects haven't
    # been implemented, and T is instead to determine how long an image should stay up for.

    # Same as the real send function, this function takes a pandas dataframe (2D matrix) of RGB values and then
    # displays them on your computer.

    global window
    global start
    global length
    global tri
    window = py.display.set_mode((700, 600))        # Initalize pygame settings, such as window size and some logic.
    length = 50
    start = [length/2,length/2]
    tri = []
    py.init()
    while True:
        for event in py.event.get():
            if event.type == py.QUIT:               # Handle what happens if the window is closed by the user while running.
                py.quit()                           # Without this, pygame will run into some issues.
            else:
                window.fill(0xFFFFFF)
                for j in range(12):
                    for i in range(26):
                            if(j%2 == 0):
                                if i%2 == 0: drawTris(i, j, False)
                                else: drawTris(i, j, True)              # Here we first draw the triangles that will be filled
                            else:                                       # with colour in the next block of code.
                                if i%2 == 0: drawTris(i, j, True)
                                else: drawTris(i, j, False)

                n = 0
                for j in range(12):
                    offset = skip[j]                                    # Here we fill the triangles we created above with colour
                    for i in range(23-offset*2):                        # data we get from the dataframe. If we can't write a colour
                        try:                                            # for some reason, it will be made grey.
                            py.draw.polygon(window,('0x%02x%02x%02x' % df[i+offset][j]), tri[n].point)
                        except:
                            py.draw.polygon(window,('0x323232'), tri[n].point)
                        n+=1

                for j in range(12):
                    for i in range(26):
                            if(j%2 == 0):                               # Finally, we want to create another layer of triangles over
                                if i%2 == 0: drawTris(i, j, False)      # top of our filled ones to simulate the lines between panels
                                else: drawTris(i, j, True)              # on the actual nanoleaf wall.
                            else:
                                if i%2 == 0: drawTris(i, j, True)
                                else: drawTris(i, j, False)

        py.display.update()
        time.sleep(T/10)                                      # Finally, we push our updates to the pygame window and then wait T seconds
        return(True)

def gradient(colour1, colour2):
    # Returns dataframe containing a gradient of RGB values between two specified values.
    # Useful in conjunction with Pandas "combine_first()" function as a background.

    # First we calculate the difference in RGB values between the two colours
    differenceR, differenceG, differenceB = colour1[0] - colour2[0], colour1[1] - colour2[1], colour1[2] - colour2[2]

    # Next, we create a list containing another list for each row
    gradient = []
    for i in range(12): gradient.append([])

    # Finally, for each row, we fill it with 23 RGB values containing the same colour.

    step = 0
    for i in range(12):
        newRow = (int(colour1[0] - (differenceR / 12) * step), int(colour1[1] - (differenceG / 12) * step),
                  int(colour1[2] - (differenceB / 12) * step))
        for k in range(23):
            gradient[i].append(newRow)
        step += 1

    # Finally, we convert our 2D list into a Pandas dataframe so that we can useit with other Pandas functions.
    df = pd.DataFrame(gradient)
    return (df)

def display():
    img = mpimg.imread('Classic_Rainbow_Flag.png')
    print(img)

start = time.time()

redToBlue = gradient((255,0,0), (0,0,255)) # Create a gradient from Red to Blue

#show(redToBlue, 1)

#time.sleep(50)

blueToRed = gradient((0,0,255), (255,0,0))
#show(blueToRed, 50)

#input jpg image and convert to pandas dataframe for show() function
'''
img = np.array(Image.open('cloudy.jpg').resize((23,12)))
b = img.view([(f'f{i}',img.dtype) for i in range(img.shape[-1])])[...,0].astype('O')
df = pd.DataFrame(b)
'''

