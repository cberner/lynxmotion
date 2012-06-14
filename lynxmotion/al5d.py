import ssc32

BASE = 0
SHOULDER = 1
ELBOW = 2
WRIST = 3
GRIPPER = 4
WRIST_ROTATE = 5

class AL5D(object):
    def __init__(self, serial_port):
        self.ssc32 = ssc32.SSC32(serial_port)

    def init(self):
        """Moves all servos to their initial position"""
        self.ssc32.move(0, 1500)
        self.ssc32.move(1, 1500)
        self.ssc32.move(2, 700)
        self.ssc32.move(3, 1600)
        self.ssc32.move(4, 1500)
        self.ssc32.move(5, 1500)
