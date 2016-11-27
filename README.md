lynxmotion-al5d
===============

Python interface for Lynxmotion AL5D

Setup
=====

* `pip install pyserial`
* `pip install pyssc32`

Check what device it was installed under, most likely /dev/ttyUSB0, by running `dmesg` or checking what new device showed up in /dev.  Then enable reading/writing to it: `sudo chmod 666 /dev/ttyUSB0`.

Confirm that it's working by running `python lynxmotion/test.py`
