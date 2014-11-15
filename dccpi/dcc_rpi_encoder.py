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

from dcc_encoder import DCCEncoder
import dcc_rpi_encoder_c
import operator


class DCCRPiEncoder(DCCEncoder):
    """
    Uses a C extension to send the packets quickly.
    """

    def __init__(self,
                 bit_one_part_min_duration=55,  # microseconds
                 bit_one_part_max_duration=61,
                 bit_one_part_duration=58,
                 bit_zero_part_min_duration=95,
                 bit_zero_part_max_duration=9900,
                 bit_zero_part_duration=100):
        DCCEncoder.__init__(self,
                            bit_one_part_min_duration,
                            bit_one_part_max_duration,
                            bit_one_part_duration,
                            bit_zero_part_min_duration,
                            bit_zero_part_max_duration,
                            bit_zero_part_duration)

    def send_packet(self, packet, times):
        packet_string = packet.to_bit_string()
        return self.send_bit_string(packet_string, times)

    def send_packets(self, packets, times):
        packet_string = "".join(map(operator.methodcaller('to_bit_string'),
                                    packets))
        return self.send_bit_string(packet_string, times)

    def send_bit_string(self, bit_string, times):
        """
        We outsource this to our C extension which can
        reliably send the bits with the correct timing.

        Passing random length arguments to C extension functions is a pain
        except for strings. So we just pass in packets as strings...
        """
        return dcc_rpi_encoder_c.send_bit_array(bit_string,
                                                times,
                                                self.bit_one_part_duration,
                                                self.bit_zero_part_duration)
