import socket
import http.client as httplib
import json
import math
import pygame as py
import time

########################################################
#                   VARIABLES                          #
########################################################

# Contains global variables (used in multiple functions)
# TODO: Find way to programatically grab IP and authcodes.
# TODO: If no way can be foud, consider an enviroment file to store these.

# Nanoleaf OpenAPI Documentation: https://forum.nanoleaf.me/docs/openapi

API_PORT = "16021" # Default port (See Nanoleaf OpenAPI documentation)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

rows = {}
networkFailure = False
skip = [5,4,3,2,1,0,0,1,2,3,4,5]

# IP addresses of the Nanoleaf controllers currently need to be found manually through the router. This is unfortunate 😕.

ip1 = "192.168.1.14"
ip2 = "192.168.1.13"
ip3 = "192.168.1.12"
ip4 = "192.168.1.10"
ip5 = "192.168.1.11"
ip6 = "192.168.1.9"
ip7 = "192.168.1.4"
ip8 = "192.168.1.5"
ip9 = "192.168.1.3"
ip10 = "192.168.1.2"
ips = [ip1, ip2, ip3, ip4, ip5, ip6, ip7, ip8, ip9, ip10]

# Authentication keys are also required to establish connection. These can change if any students hold the physical buttons on the controllers too long.

auth1 = "LKI439ILyLPOZ73i0fOodP3rgxObe2eO"
auth2 = "Vu9ggkGI9RNQ2SDaFPNfUIa7kX9r86nq"
auth3 = "Q6hNMymIYPtuJmc8c3Ok4roVjFlFO3F7"
auth4 = "Vu9ggkGI9RNQ2SDaFPNfUIa7kX9r86nq"
auth5 = "LKI439ILyLPOZ73i0fOodP3rgxObe2eO"
auth6 = "s4R1paJWsiccOAiy2xP39yYWSAfhNmdx"
auth7 = "ALf4TvPrNiK4hxEVdjtbc5Gl0X2l0NCl"
auth8 = "eRTQpXfNZh4KLdvnJXsdQMsSzspSerPu"
auth9 = "cSTCTsuAgBRC7i8F3ug1cc1Z1smDyPQH"
auth10 = "s0M4TKH8BhTxdSIReRuAJzAHTYkHTdWU"
auths = [auth1, auth2, auth3, auth4, auth5, auth6, auth7, auth8, auth9, auth10]

########################################################
#               NETWORKING FUNCTIONS                   #
########################################################

# Contains functions nessescary for networking, taken from old file.

def setStreamControlMode(ip, auth, version):
    '''
    Enables stream control mode on the Nanoleaf device version should be 1, all controllers need to be set to send commands
    Section 3.2.6.2 "External Control (extControl)" && Section 5.7 "External Control (Streaming)"
    '''
    end_point = "/api/v1/" + auth + "/effects"
    ext_control_version = "v" + str(version)
    ext_control_command = {
        'write': {'command': 'display', 'animType': 'extControl', 'extControlVersion': ext_control_version}}
    status, __, __ = sendAPI("PUT", end_point, json.dumps(ext_control_command), ip)  # json.dumps() changes the python dictionary into a json object that the nanoleaf panels can understand.
    if not (status == 200 or status == 204):                                         # The opposite can be acheived with json.loads() which converts a json object to a python dictionary.
        print("Could not connect: " + str(status))

def sendAPI(verb, endpoint, body, ip):
    '''
    Sends an API command to the Nanoleaf device at a given IP address using the formatting in the open API
    '''
    LISTENER = ip + ":" + API_PORT
    try:
        conn = httplib.HTTPConnection(LISTENER)
        if len(body) != 0:
            conn.request(verb, endpoint, body, {"Content-Type": "application/json"})
        else:
            conn.request(verb, endpoint)
        response = conn.getresponse()
        body = response.read()
        return response.status, response.reason, body  
        # Status is equivalent to the 200 phrase in the Nanoleaf OpenAPI documentation.
        # Reason is the text next to the number (OK, No Content, etc.) body, as defined in the line above is found using the .read() method, 
        # and returns the response body as defined in Nanoleaf OpenAPI documentation.
    except (httplib.HTTPException, socket.error) as ex:
        print("Error: %s" % ex)

def getDeviceData(ip, auth):
    '''
    Gets all panel info from the Nanoleaf device, returns in the format of the API JSON in the documentation
    can be accessed using json.loads() to create a dictionary, then accessed by using regular python dictionary syntax

    Section 4.1 "API JSON Structure > Light Panels"
    '''
    endpoint = "/api/v1/" + auth
    status, __, body = sendAPI("GET", endpoint, {}, ip)  # Body is the json object containing information about the controller as detailed in section 4.1 of the Nanoleaf OpenAPI documentation.
    if not status == 200:
        print("Could not connect: " + str(status))
    return body

def sendStreamControlFrames(frames, ip):
    '''
    frames: An array of frames, with each frame consisting of a dictionary with the panelId and the color
    the panel must go to in the specified time. Color is specified as R, G, B and transTime (T) in multiples of 100ms.

    Section 3.2.6.2 "External Control (extControl)" && Section 5.7 "External Control (Streaming)"
    '''
    stream = bytearray()
    stream.append(len(frames) & 0xFF)
    # Port is 60221 for v1 (original Light Panels), v2 for newer products (Shapes, Elements, Canvas) NOT USED IN OUR ARRAY
    # This port number can be found by returning the body in the setStreamControlMode function.
    port = 60221
    for frame in frames:
        stream.append(frame['panelId'] & 0xFF)  # Python integers are 32 bits, but RGB values are only 8 bits. This & 0xFF term converts our python int to an 8 bit binary value.
        stream.append(1 & 0xFF)                 # For example, 158 would be 10011110 (Hexadecimal 0x9E)
        stream.append(frame['R'] & 0xFF)
        stream.append(frame['G'] & 0xFF)
        stream.append(frame['B'] & 0xFF)
        stream.append(0 & 0xFF)  # White channel is controlled by the panel itself, setting it manually slows down the process. We still need to include it in the bytestream, though.
        stream.append(frame['T'] & 0xFF)

    # Why does this need to happen? Well, we're sending the data as a byte stream, aka a list of numbers. 
    # So, we need to convert our current frame in the form {'panelId': id, 'R': 255, 'G': 255, 'B': 255, 'W': 0, 'T': 1}
    # into a byte stream, which would look like "0x00 0x03 0x01 0x76 0xFF 0x00 0xFF 0x00 0x00 0xC 0x02 0x8B 0xFF 0xFF
    # 0x00 0x00 0x00 0x80 0x00 0xEB 0x00 0xFF 0xFF 0x00 0x01 0xC3". We do this using a bitwise AND (&) operator which takes two binary
    # numbers and returns 1 if they are both 1 in the same position (i.e 0110 & 0101 would be 0100). 0xFF is 11111111 in binary.

    # Why do we send information in byte streams? Because we can only send a 1 or a 0 (technically not correct, but essentially correct)
    # which means we need a way to represent information in that form. We use 8 binary bits to represent a byte, which can represent a
    # number between 0 and 254 (255 values) which we can assign to something like a letter, Google "ASCII values" to see this in action!

    sock.sendto(stream, (ip, port))

def getPanelIDs(ip, auth):
    # Function takes an IP and an authorization code, requests the dictionary from the OpenAPI (see section 4.1 for json structure) and grabs the panel ID for each
    # light panel for the controller at that IP. Returns a list of panel IDs in the order they're physically attached to the controller.
    panelIDs = []
    controller = json.loads(getDeviceData(ip, auth))
    controllerData = controller['panelLayout']['layout']['positionData'] # If you'd like to see why this format is used, see Nanoleaf OpenAPI Documentation section 4.1
    for index in range(len(controllerData)):
        panelIDs.append(controllerData[index]['panelId'])
    return panelIDs

########################################################
#               ABSTRACTION FUNCTIONS                  #
########################################################

# Contains functions designed to make the process easier for students, abstracting away much of the boilerplate code into two functions.
# TODO: If method is discovered for discovering IP and auth automatically, include in initiate()

def initalize(verbose = False):
    # Initalizes the connection to each controller, and grabs the PanelIDs for each controller and sorts them into their correct
    # rows, avoiding the problem with controllers 1 and 10 controlling multiple rows. Returns true to indicate succcess.
    # Takes a boolean value to determine if it should print where it's at in the process (default = False)

    # If this function cannot connect to the panels, it will instead set the 'networkFailure' flag to 'True' which will

    if verbose: print("Starting initalization...", flush=True)
    global networkFailure
    global rows
    rows = []

    try:
        for i in range(len(ips)):
                # This has to be set to control the panels remotely (external streaming control)
                setStreamControlMode(ips[i], auths[i], 1)
                if verbose: print("Connected to controller {} at IP address: {}".format(i+1, ips[i]), flush=True)
    except:
        if verbose: print("Could not find devices on network. Redirecting send function to simulator!", flush=True)
        networkFailure = True
        return False

    # Here we're using the prior knowledge that Nanoleaf controllers store panel IDs in the order they're physically connected (branches are an exception) in
    # order to sort panels into an ascending list we can access to make it easier to assign RGB values to the correct panel.
    for i in range(0,10):
        if verbose: print("Grabbing IDs for controller {}".format(i+1), flush=True)
        controllerPanelIDs = getPanelIDs(ips[i], auths[i])
        if i == 0:
            rows[0] = list(reversed(controllerPanelIDs[14:27]))
            rows[1] = controllerPanelIDs[0:14]
            rows[1].append(controllerPanelIDs[27])
        elif i == 9:
            rows[11] = list(reversed(controllerPanelIDs[14:27]))
            rows[10] = controllerPanelIDs[0:14]
            rows[10].append(controllerPanelIDs[27])
        else:
            rows[i + 1] = controllerPanelIDs
    if verbose: print("Initalization complete.", flush=True)
    return True

def send(df, time = 1):   
    # Takes in a 2D Matrix (pandas dataframe) of size 23x12 and converts it's X/Y form into the associated panel IDs for the
    # nanoleaf wall. It then sends everything to the wall. Returns nothing. Additional argument for transition time T (T is in units of 1/10th of a second).
    allframes = [[],[],[],[],[],[],[],[],[],[]]

    if networkFailure:              # If we failed to connect to the panels when we ran Initalize(), redirect
        simSend(df, time)           # the dataframe to the simulator.
        return(True)

    # Using the knowledge that the panels are 12 high and 23 wide at their extremes, we can skip the first N spaces in our matrix (represented using 'offset')
    # and the PanelIDs we found in initalize() to assign X/Y values from the matrix onto the nanoleaf wall.
    print(rows)
    for i in range(0,12):
        offset = skip[i]
        for k in range(0,(23-offset*2)):
            if df[k+offset][i] != None:
                currentFrame = {'panelId': rows[i][k], 'R': df[k+offset][i][0], 'G': df[k+offset][i][1], 'B': df[k+offset][i][2], 'T': time}
                if i == 0:
                    allframes[0].append(currentFrame)
                elif i == 1:
                    allframes[0].append(currentFrame)
                elif i == 10:
                    allframes[9].append(currentFrame)
                elif i == 11:
                    allframes[9].append(currentFrame)
                else:
                    allframes[i-1].append(currentFrame)

    # We then send each "frame" (i.e list of dictionaries containing panel and RGB information) to the associated controller.
    for i, single in enumerate(allframes):
        if single != []:    
            sendStreamControlFrames(single, ips[i])
    return(True) # Return True so we can detect when it's done sending if needed.


########################################################
#                     SIMULATOR                        #
########################################################

#               Author: Maxwell McEvoy                 #

# The following code was created by Maxwell McEvoy for the September 2022 hackathon and
# was modified to accept the same dataframe format as the "send" function in this file.
# Modifications have been made to Maxwell's code to make this section smaller.

def simSend(df, T = 5):
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
        return(True)                                       # before returning true to indicate a success.
   
def drawTris(i, j, pointsDown):
    # This function determines uses the oriantation information provided by "pointsDown" to draw a triangle
    # at the specified i (column) and j (row) index.
    iteration = 1
    if pointsDown: iteration = 0                    

    if j < 6 and i >= 6-j and i <= 18+j:
        mid = [start[0]+length/2*i, start[1]+(length*j)]
        tri.append(Triangle(mid, pointsDown, length, 0x000000))
        py.draw.polygon(window,0x0, tri[-1].point, 1)

    if j >= 6 and (i > iteration+(j-6) and i < 26 - (j-4)):
        mid = [start[0]+length/2*i, start[1]+(length*j)]
        tri.append(Triangle(mid, pointsDown, length,0x000000))
        py.draw.polygon(window,0x0, tri[-1].point, 1)

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
        Ay = mid[1] - (math.cos(60)*length) / 2
        By = Ay
        Cy = Ay + math.cos(60)*length
        return [(Ax,Ay), (Bx,By), (Cx, Cy)]

    def __invtri__(self, mid, length):
        # Calculates the three vertext points of a equalateral triangle point down.
        Ax = mid[0] - length / 2
        Bx = mid[0] + length / 2
        Cx = mid[0]
        Ay = mid[1] + (math.cos(60)*length) / 2
        By = Ay
        Cy = Ay - math.cos(60)*length
        return [(Ax,Ay), (Bx,By), (Cx, Cy)]

    def set_color(self, color): self.color = color          # Get/Set functions
    def get_color(self): return self._color

