import al5d
import math

#Gripper height when drawing
HEIGHT = -0.026
#Gripper angle when drawing
PHI = -math.pi / 5

class Drawing(object):
    def __init__(self, serial_port='/dev/ttyUSB0'):
        self.al5d = al5d.AL5D(serial_port=serial_port)

    def init(self):
        self.al5d.init()
        self.al5d.move(0, 0.2, HEIGHT, PHI)
        print "Please place the pen"

    def grip_pen(self):
        self.al5d.gripper(72)

    def rect(self, upper_left, lower_right):
        self.line(upper_left[0], upper_left[1], lower_right[0], upper_left[1])
        self.line(lower_right[0], upper_left[1], lower_right[0], lower_right[1])
        self.line(lower_right[0], lower_right[1], upper_left[0], lower_right[1])
        self.line(upper_left[0], lower_right[1], upper_left[0], upper_left[1])

    def path(self, coords):
        """coords: list of (x, y) tuples"""
        self.al5d.move(0, 0.2, 0.1, PHI)
        self.al5d.wait_for_move()
        self.al5d.move(coords[0][0], coords[0][1], HEIGHT + 0.02, PHI)
        self.al5d.wait_for_move()
        
        for i in range(len(coords) - 1):
            start_x = coords[i][0]
            start_y = coords[i][1]
            end_x = coords[i + 1][0]
            end_y = coords[i + 1][1]

            distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
            #Take steps that are 0.5mm
            num_steps = int(distance * 2000)
            
            #Parameterize x and y in terms of t
            slope_x = (end_x - start_x) / num_steps
            slope_y = (end_y - start_y) / num_steps
            for t in range(num_steps):
                self.al5d.move(start_x + t*slope_x, start_y + t*slope_y, HEIGHT, PHI)
                self.al5d.wait_for_move()

            #Make sure we end exactly where requested
            #(num_steps is descretized so we might not)
            self.al5d.move(end_x, end_y, HEIGHT, PHI)
            self.al5d.wait_for_move()

        #Lift pen straight up, before returning to home position
        self.al5d.move(coords[-1][0], coords[-1][1], HEIGHT + 0.02, PHI)
        self.al5d.wait_for_move()
        self.al5d.move(0, 0.2, 0.1, PHI)
        self.al5d.wait_for_move()


    def line(self, start_x, start_y, end_x, end_y):
        self.path(((start_x, start_y), (end_x, end_y)))
