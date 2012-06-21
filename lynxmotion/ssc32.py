import serial

class SSC32(object):
    def __init__(self, serial_port):
        self.serial = serial.Serial(serial_port, 115200)
        self.in_group = False

    def write(self, string):
        """Sends the given string to the SSC-32 controller.

        string: does not need to end with a \r character"""
        self.serial.write(string + "\r")

    def readline(self):
        s = ""
        while True:
            b = self.serial.read()
            if b == '\r':
                break
            s += b
        return s

    def version(self):
        self.write("VER")
        return self.readline()

    def move_done(self):
        self.write("Q")
        return self.serial.read() == "."

    def move(self, servo, pulse_width, speed=None, time=None):
        """Moves the given servo.

        servo: an integer indicating which servo to move
        pulse_width: an integer in [500, 2500], indicating the pulse width to move to
        speed: speed in uS to move at
        time: the desired time in seconds that the move should take"""
        assert 500 <= pulse_width <= 2500, pulse_width
        assert 0 <= servo <= 31, servo

        command = "#{servo} P{pulse_width}".format(servo=servo, pulse_width=pulse_width)
        if speed:
            command += " S{speed}".format(speed=speed)
        if time:
            command += " T{time}".format(time=int(1000*time))
        if self.in_group:
            self.group += " " + command
        else:
            self.write(command)

    def move_group(self):
        """Returns a context manager for performing several movements as a group

        All calls to .move() in this block, will be executed at the same time"""
        return self

    def __enter__(self):
        self.in_group = True
        self.group = ""

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value:
            raise exc_value, None, traceback
        self.in_group = False
        assert self.group, "Empty group"
        self.write(self.group)
