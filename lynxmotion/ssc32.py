import serial

class SSC32(object):
    def __init__(self, serial_port):
        self.serial = serial.Serial(serial_port, 115200)

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

    def move(self, servo, pulse_width, speed=None, time=None):
        """Moves the given servo.

        servo: an integer indicating which servo to move
        pulse_width: an integer in [500, 2500], indicating the pulse width to move to
        speed: speed in uS to move at
        time: the desired time in ms that the move should take"""
        assert 500 <= pulse_width <= 2500, pulse_width
        assert 0 <= servo <= 31, servo

        command = "#{servo} P{pulse_width}".format(servo=servo, pulse_width=pulse_width)
        if speed:
            command += " {speed}".format(speed=speed)
        if time:
            command += " {time}".format(time=time)
        self.write(command)

