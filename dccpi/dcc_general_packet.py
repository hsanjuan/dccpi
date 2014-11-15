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


class DCCGeneralPacket(object):
    """
    A class to build any DCC packet given an address and data bytes
    """
    def __init__(self,
                 address_byte,
                 data_bytes=[]):
        """
        All arguments simle binary/hex strings: 0xFF 0b2121
        """
        self.preamble = BitArray('0b111111111111')
        self.packet_start_bit = BitArray('0b0')
        self.address_byte = BitArray(address_byte)
        self.data_byte_start_bit = BitArray('0b0')
        self.data_bytes = map(BitArray, data_bytes)
        self.packet_end_bit = BitArray('0b1')

        assert(len(self.address_byte) == 8)
        for byte in self.data_bytes:
            assert(len(byte) == 8)

    @staticmethod
    def from_bit_array(int_array):
        """
        Given [1, 1,...] array try to decode a packet
        """
        packet = BitArray(int_array)
        # preamble = packet[0:12]
        address_byte = packet[13:21]
        data_bytes = packet[22:-1]
        dbit = 0
        data_bytes_a = []
        while dbit < len(data_bytes):
            data_bytes_a.append(data_bytes[dbit:dbit+8])
            dbit += 9  # skip start bit from next data byte
        return DCCGeneralPacket(address_byte, data_bytes_a)

    def to_bit_array(self):
        """
        Builds a single string that should end up
        being serialized.

        Returns an array of True/False
        """
        packet = BitArray()
        packet.append(self.preamble)
        packet.append(self.packet_start_bit)
        packet.append(self.address_byte)
        for byte in self.data_bytes:
            packet.append(self.data_byte_start_bit)
            packet.append(byte)
        packet.append(self.packet_end_bit)
        return map(int, packet)

    def to_bit_string(self):
        return "".join(map(str, self.to_bit_array()))

    def __str__(self):
        """
        Allow some debuging
        """
        if len(self.data_bytes) > 2:
            return "Device #%d: %s" % (self.address_byte.uint,
                                       " ".join(map(str, self.data_bytes)))
        else:  # Assume this is a baseline packet
            string = "Device #%d: Dir->%d, HL->%d, Speed->%d"
            instruction = self.data_bytes[0]
            direction = instruction[2:3].uint
            headlight = instruction[3:4].uint
            speed = instruction[4:8].uint
            return string % (self.address_byte.uint,
                             direction, headlight, speed)
