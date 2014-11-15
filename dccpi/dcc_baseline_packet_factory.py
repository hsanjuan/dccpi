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

from bitstring import BitArray
from dcc_general_packet import DCCGeneralPacket


class DCCBaselinePacketFactory:
    """
    Make it easy to build Baseline packages types
    """
    @staticmethod
    def speed_and_direction_packet(address,
                                   speed,
                                   headlight_on,
                                   direction,
                                   headlight_support=True):
        """
        Build a speed and direction packet.

        param address int is the dcc device address.
        param speed   int is the speed:
            * 0 - Stop
            * 1 - Stop (I) (headlights disabled)
            * 2 - Emergency-Stop
            * 3 - Emergency-Stop (I) (headlights disabled)
            * 4..31 - Step 1..Step 28 or 1-14
        param headlight_on bool decides if headlight is turned on when
              supported
        param direction int is 1 for forward and 0 for backwards.
        param headlight_support decides if we use 16 or 32 speed steps
        """
        address_bin = BitArray('uint:8=%d' % address)
        instruction_bin = BitArray('0b01')
        if direction:
            instruction_bin.append('0b1')
        else:
            instruction_bin.append('0b0')

        if headlight_support:
            if headlight_on:
                instruction_bin.append('0b1')
            else:
                instruction_bin.append('0b0')
            speed_bin = BitArray('uint:4=%d' % speed)
            instruction_bin.append(speed_bin)
        else:
            speed_bin = BitArray('uint:5=%d' % speed)
            speed_bin.ror()
            instruction_bin.append(speed_bin)

        error = address_bin ^ instruction_bin

        data = [instruction_bin, error]
        return DCCGeneralPacket(address_bin, data)

    @staticmethod
    def reset_packet():
        """
        Build a reset package for all decoders.

        All decoders shall erase all volatile memory, return
        to power-up state and bring locomotives to an immediate
        stop.
        """
        byte_one = BitArray('0b00000000')
        byte_two = BitArray('0b00000000')
        byte_three = BitArray('0b00000000')
        return DCCGeneralPacket(byte_one, [byte_two, byte_three])

    @staticmethod
    def idle_packet():
        """
        Build an idle packet for all decoders.

        Upon receiving, all decoders shall perform no new action and act
        like if it was a packet addressed to some other decoder.
        """
        byte_one = BitArray('0b11111111')
        byte_two = BitArray('0b00000000')
        byte_three = BitArray('0b11111111')
        return DCCGeneralPacket(byte_one, [byte_two, byte_three])

    @staticmethod
    def stop_packet(direction=1,
                    soft_stop=False,
                    ignore_direction=True):
        """
        Build a stop packet for all decoders.

        param direction sets the direction bit in the packet.
        param soft_stop indicates if the decoder bring the locomotive to stop
                        or stop delivering energy to the engine (guess in
                        the first case it may gradually decelerate it)
        param ignore_direction allows optionally ignoring the direction bit
                               for all direction sensitive functions
        """
        byte_one = BitArray('0b00000000')
        byte_two = BitArray('0b01')
        if direction:
            byte_two.append('0b1')
        else:
            byte_two.append('0b0')
        if ignore_direction:
            byte_two.append('0b1')
        else:
            byte_two.append('0b0')

        byte_two.append('0b000')

        if soft_stop:
            byte_two.append('0b0')
        else:
            byte_two.append('0b1')

        byte_three = byte_two.copy()
        return DCCGeneralPacket(byte_one, [byte_two, byte_three])
