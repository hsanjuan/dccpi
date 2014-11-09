NRMA Digical Command Control (DCC) implementation for Raspberry Pi
==================================================================

*Development status: alpha, unstable, unstested.*

This module implements the DCC protocol for controlling model trains using a RaspberryPi.

It is able to output direction and speed DCC-encoded packets on one of the GPIO pins (see example below) by using a small wiringPi-based C extension.

It is based on the:
  * [S-91 Electrical Standard](http://www.nmra.org/sites/default/files/standards/sandrp/pdf/s-9.1_electrical_standards_2006.pdf)
  * [S-92 DCC Communications Standard](http://www.nmra.org/sites/default/files/s-92-2004-07.pdf)

Features
--------

  * Control DCC locomotives using Python
  * Set speed, direction and lights

Hardware requirements
---------------------

  * A Raspberry Pi (developed/tested on model B+)
  * The Raspberry Pi needs an additional booster circuit to actually provide the signal to the tracks (working on that).

Software requirements
---------------------

  * wiringPi: download and install [wiringPi](http://wiringpi.com/download-and-install/)
  * Since wiringPi uses low-level mechanisms to access pins, dccpi programs **must be run as root**

Installation
------------

From PyPI:

`sudo pip install dccpi`

From Source:

`sudo python setup.py install`

Usage
-----

There are 3 main componenents:

  * `DCCLocomotive`: represents a locomotive (device equipped with a DCC decoder). We can set speed, status of lights etc.
  * `DCCController`: represents the command station, that can be turned on/off. When it's on, it sends packets using a DCCEncoder.
  * `DCCRPiEncoder`: it implements methods to actually send packets. The RPi encoder uses a c-extension to do it. It should be easy to add other encoders (for example to different platforms than the RPi).

The Raspberry Pi will output the signal (which goes from 0v-Low to 3.3v-High) onBCM GPIO pin 17, which is Physical Pin 11 (Model B+), which is wiringPi pin 0.

See example below and read the code for more info.

Example
-------

    from dccpi import *

    encoder = DCCRpiEncoder()
    controller = DCCController(encoder)
    loco1 = DCCLocomotive(name="my loco", address=3, speed=0)
    controller.register(loco1)
    controller.start()
    # The encoder sends the packets on a different thread
    loco1.faster()
    # ...
    loco1.set_speed(7)
    # ...
    loco1.stop()
    # ...
    controller.stop()

Example with dummy encoder
--------------------------

Same as above but pass `DCCDummyEncoder()` to the controller. The Dummy Encoder will print information to the screen every 10 seconds on what packages are sent and to who, but leave GPIO outputs alone.
