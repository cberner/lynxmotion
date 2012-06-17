import ssc32
import math

BASE = 0
SHOULDER = 1
ELBOW = 2
WRIST = 3
GRIPPER = 4
WRIST_ROTATE = 5


#Measured from bottom of base to servo center, in meters
SHOULDER_HEIGHT = 0.06985
#Measured from servo centers, in meters
SHOULDER_ELBOW_LENGTH = 0.14605
#Measured from servo centers, in meters
ELBOW_WRIST_LENGTH = 0.20955

#XXX: All interpolation is specific to my arm
class AL5D(object):
    def __init__(self, serial_port):
        self.ssc32 = ssc32.SSC32(serial_port)

    def init(self):
        """Moves all servos to their initial position"""
        self.ssc32.move(1, 1500)
        self.ssc32.move(2, 700)
        self.ssc32.move(3, 1600)
        self.ssc32.move(5, 1500)
        self.move(0, 0.2, 0.2)
        self.gripper(50)

    def move(self, x, y, z):
        """Moves the arm to the given coordinate
        x, y, z given in meters"""
        #Compute the base rotation
        if x or y:
            base_angle = math.atan2(y, x)
            self.base(base_angle)

        #Distance from center of base
        d = math.sqrt(x**2 + y**2)
        #Height above shoulder joint
        z_prime = z - SHOULDER_HEIGHT

        l1 = SHOULDER_ELBOW_LENGTH
        l2 = ELBOW_WRIST_LENGTH
        #Compute the elbow angle
        numerator = d**2 + z_prime**2 - l1**2 - l2**2
        denominator = 2*l1*l2
        elbow_theta = math.atan2(math.sqrt(1 - (numerator / denominator)**2), numerator / denominator)
        #There are two possible solutions (one in which in the elbow is bending "backwards")
        if elbow_theta > 0:
            elbow_theta = math.atan2(-math.sqrt(1 - (numerator / denominator)**2), numerator / denominator)
        #Our angles are measured the opposite direction
        self.elbow(-elbow_theta)

        #Compute the shoulder angle
        k1 = l1 + l2 * math.cos(elbow_theta)
        k2 = l2 * math.sin(elbow_theta)
        shoulder_theta = math.atan2(z_prime, d) - math.atan2(k2, k1)
        self.shoulder(math.pi / 2 - shoulder_theta)

    def gripper(self, percent, speed=100, time=None):
        """Open/close the gripper
        
        percent (float): the percentage closed that the gripper should be (100% is closed, 0% is open)"""
        assert 0 <= percent <= 100, percent
        self.ssc32.move(GRIPPER, int(1100 + 900*(percent / 100.0)), speed, time)

    def base(self, angle, speed=100, time=None):
        """Rotate the base

        angle: the angle to rotate to [0, pi], positive angles are counter-clockwise. 
        pi/2 is facing directly away from controller board"""
        assert 0 <= angle <= math.pi, angle
        percent = angle / math.pi
        self.ssc32.move(BASE, int(2300 - 1800*percent), speed, time)

    def shoulder(self, angle, speed=100, time=None):
        """Move the shoulder

        angle: the angle to rotate to [-pi/4, pi/4], positive angles are counter-clockwise 
        when viewed from the top of the servo. 0 is pointing straight up"""
        assert -math.pi / 4 <= angle <= math.pi / 4, angle
        percent = angle / (math.pi / 4)
        self.ssc32.move(SHOULDER, int(1500 - 400*percent), speed, time)

    def elbow(self, angle, speed=100, time=None):
        """Move the elbow

        angle: the angle to rotate to [0, pi/2], positive angles are counter-clockwise 
        when viewed from the top of the servo. 0 has the arm fully extended"""
        assert 0 <= angle <= math.pi / 2, angle
        percent = angle / (math.pi / 2)
        self.ssc32.move(ELBOW, int(700 + 700*percent), speed, time)

    def wrist(self, angle, speed=100, time=None):
        """Move the wrist

        angle: the angle to rotate to [-pi/4, pi/4], positive angles are counter-clockwise 
        when viewed from the top of the servo. 0 is fully extended"""
        assert -math.pi / 4 <= angle <= math.pi / 4, angle
        percent = angle / (math.pi / 4)
        self.ssc32.move(WRIST, int(1550 - 400*percent), speed, time)

    def wrist_rotate(self, angle, speed=100, time=None):
        """Rotate the wrist

        angle: the angle to rotate to [-pi/4, pi/4], positive angles are counter-clockwise 
        when viewed looking into the gripper"""
        assert -math.pi / 4 <= angle <= math.pi / 4, angle
        percent = angle / (math.pi / 4)
        self.ssc32.move(WRIST_ROTATE, int(1450 + 500*percent), speed, time)



