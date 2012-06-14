import ssc32
import math

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

    def gripper(self, percent, speed=None, time=5.0):
        """Open/close the gripper
        
        percent (float): the percentage closed that the gripper should be (100% is closed, 0% is open)"""
        assert 0 <= percent <= 100
        #XXX: This interpolation is specific to my arm
        self.ssc32.move(GRIPPER, int(1100 + 900*(percent / 100.0)), speed, time)

    def base(self, angle, speed=None, time=5.0):
        """Rotate the base

        angle: the angle to rotate to [-pi/2, pi/2], positive angles are counter-clockwise. 
        0 is facing directly away from controller board"""
        assert -math.pi / 2 <= angle <= math.pi / 2
        percent = angle / (math.pi / 2)
        self.ssc32.move(BASE, int(1400 - 900*percent), speed, time)

    def shoulder(self, angle, speed=None, time=5.0):
        """Move the shoulder

        angle: the angle to rotate to [-pi/4, pi/4], positive angles are counter-clockwise 
        when viewed from the top of the servo. 0 is pointing straight up"""
        assert -math.pi / 4 <= angle <= math.pi / 4
        percent = angle / (math.pi / 4)
        self.ssc32.move(SHOULDER, int(1500 - 400*percent), speed, time)

    def elbow(self, angle, speed=None, time=5.0):
        """Move the elbow

        angle: the angle to rotate to [0, pi/2], positive angles are counter-clockwise 
        when viewed from the top of the servo. 0 has the arm fully extended"""
        assert 0 <= angle <= math.pi / 2
        percent = angle / (math.pi / 2)
        self.ssc32.move(ELBOW, int(700 + 700*percent), speed, time)

    def wrist(self, angle, speed=None, time=5.0):
        """Move the wrist

        angle: the angle to rotate to [-pi/4, pi/4], positive angles are counter-clockwise 
        when viewed from the top of the servo. 0 is fully extended"""
        assert -math.pi / 4 <= angle <= math.pi / 4
        percent = angle / (math.pi / 4)
        self.ssc32.move(WRIST, int(1550 - 400*percent), speed, time)

    def wrist_rotate(self, angle, speed=None, time=5.0):
        """Rotate the wrist

        angle: the angle to rotate to [-pi/4, pi/4], positive angles are counter-clockwise 
        when viewed looking into the gripper"""
        assert -math.pi / 4 <= angle <= math.pi / 4
        percent = angle / (math.pi / 4)
        self.ssc32.move(WRIST_ROTATE, int(1450 + 500*percent), speed, time)



