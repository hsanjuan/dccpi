"""
    Copyright (C) 2014  Hector Sanjuan

    This file is part of "dccpi".

    "dccpi" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "dccpi" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""

from dcc_baseline_packet_factory import DCCBaselinePacketFactory


class DCCLocomotive(object):
    """
    A locomotive is a thing with speed, direction and lights
    """
    def __init__(self,
                 name,
                 address,
                 speed=0,
                 direction=1,
                 headlight_on=False,
                 headlight_support=True):
        self.name = name
        self.address = address
        self.direction = direction
        self.headlight_on = headlight_on,
        self.headlight_support = headlight_support

        self.set_speed(speed)

    def emergency_stop(self):
        self.speed = 1

    def stop(self):
        self.speed = 0

    def reverse(self):
        self.direction = 0 if (self.direction) else 1

    def turn_headlight_on(self):
        self.headlight_on = True

    def turn_headlight_off(self):
        self.headlight_on = False

    def switch_headlight(self):
        self.headlight_on = False if (self.headlight_on) else True

    def slower(self):
        # Skip emergency stop
        if self.speed is 2:
            self.set_speed(0)
        else:
            self.set_speed(self.speed - 1)

    def faster(self):
        if self.speed is 0:
            self.set_speed(2)
        else:
            self.set_speed(self.speed + 1)

    def set_speed(self, speed):
        # Make some basic checks
        speed = abs(speed)
        if self.headlight_support:
            self.speed = min(15, speed)
        else:
            self.speed = min(31, speed)

    def control_packet(self):
        factory = DCCBaselinePacketFactory
        return factory.speed_and_direction_packet(self.address,
                                                  self.speed,
                                                  self.headlight_on,
                                                  self.direction,
                                                  self.headlight_support)
