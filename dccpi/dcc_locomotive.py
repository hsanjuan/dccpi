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
        self._address = address
        self.direction = direction
        self._headlight_on = headlight_on,
        self.headlight_support = headlight_support

        # We need a way to tell controller to update the payload
        # everytime we modify something
        # This will be set by the controller
        self.notify_update_callback = None

        self.speed = speed

    def emergency_stop(self):
        self.speed = 1
        self._notify_update()

    def stop(self):
        self.speed = 0
        self._notify_update()

    def reverse(self):
        self.direction = 0 if (self.direction) else 1
        self._notify_update()

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        # Make some basic checks
        speed = abs(speed)
        if self.headlight_support:
            self._speed = min(15, speed)
        else:
            self._speed = min(31, speed)
        self._notify_update()

    @property
    def headlight_on(self):
        return self._headlight_on

    @headlight_on.setter
    def headlight_on(self, x):
        self._headlight_on = x
        self._notify_update()

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, ad):
        self._address = ad
        self._notify_update()

    def turn_headlight_on(self):
        self.headlight_on = True
        self._notify_update()

    def turn_headlight_off(self):
        self.headlight_on = False
        self._notify_update()

    def switch_headlight(self):
        self.headlight_on = False if (self.headlight_on) else True

    def slower(self):
        # Skip emergency stop
        if self.speed is 2:
            self.speed = 0
        else:
            self.speed = (self.speed - 1)

    def faster(self):
        # Skip emergency stop
        if self.speed is 0:
            self.speed = 2
        else:
            self.speed = (self.speed + 1)

    def control_packet(self):
        factory = DCCBaselinePacketFactory
        return factory.speed_and_direction_packet(self.address,
                                                  self.speed,
                                                  self.headlight_on,
                                                  self.direction,
                                                  self.headlight_support)

    def _notify_update(self):
        """
        Used by the DCC controller to generate a new set
        of packets with updated information for the encoder
        """
        if self.notify_update_callback:
            self.notify_update_callback(self.name)
