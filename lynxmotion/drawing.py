import al5d
import math

#Gripper height when drawing
HEIGHT = -0.01

class Drawing(object):
    def __init__(self, serial_port='/dev/ttyUSB0'):
        self.al5d = al5d.AL5D(serial_port=serial_port)

    def init(self):
        self.al5d.init()
        self.al5d.move(0, 0.2, HEIGHT)
        print "Please place the pen"

    def grip_pen(self):
        self.al5d.gripper(78)

    def line(self, start_x, start_y, end_x, end_y):
        self.al5d.move(0, 0.2, 0.1)
        self.al5d.wait_for_move()
        self.al5d.move(start_x, start_y, HEIGHT + 0.02)
        self.al5d.wait_for_move()

        distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        #Take steps that are 0.5mm
        num_steps = int(distance * 2000)
        
        #Parameterize x and y in terms of t
        slope_x = (end_x - start_x) / num_steps
        slope_y = (end_y - start_y) / num_steps
        for t in range(num_steps):
            self.al5d.move(start_x + t*slope_x, start_y + t*slope_y, HEIGHT)
            self.al5d.wait_for_move()

        #Make sure we end exactly where requested
        #(num_steps is descretized so we might not)
        self.al5d.move(end_x, end_y, HEIGHT)
        self.al5d.wait_for_move()
        #Lift pen straight up, before returning to home position
        self.al5d.move(end_x, end_y, HEIGHT + 0.02)
        self.al5d.wait_for_move()
        self.al5d.move(0, 0.2, 0.1)
        self.al5d.wait_for_move()
