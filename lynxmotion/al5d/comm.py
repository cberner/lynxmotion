import subprocess

class SCC32SerialConnection(object):
    def __init__(self, serial_port):
        """serial_port: path to device (i.e. /dev/ttyUSB0)"""
        self.fd = open(serial_port, 'r+')
        #XXX: This should really be done with termios
        #Set all the necessary serial options
        subprocess.call(('stty -F /dev/ttyUSB0 115200 ignbrk -brkint -icrnl' +\
            ' -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok' +\
            ' -echoctl -echoke min 1 time 5').split(' '))

    def send(self, command):
        """command: the string to send (*not* terminated with a newline character)"""
        self.fd.write(command + "\r\n")

    def receive(self):
        return self.fd.read()

t = SCC32SerialConnection('/dev/ttyUSB0')
