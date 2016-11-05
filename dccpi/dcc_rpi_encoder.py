"""
    Copyright (C) 2016  Hector Sanjuan

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
    along with "dccpi".  If not, see <http://www.gnu.org/licenses/>.
"""

from .dcc_encoder import DCCEncoder
import dcc_rpi_encoder_c
import operator


class DCCRPiEncoder(DCCEncoder):
    """
    This encoder uses dcc_rpi_encoder_c extension to modify GPIO pins and
    encode 0 and 1 bits according to DCC.

    It also saves they payload as a string, as this is the format passed
    to the extension, so it does not have to be rebuilt everytime.
    """

    def __init__(self,
                 bit_one_part_min_duration=55,  # microseconds
                 bit_one_part_max_duration=61,
                 bit_one_part_duration=58,
                 bit_zero_part_min_duration=95,
                 bit_zero_part_max_duration=9900,
                 bit_zero_part_duration=100,
                 packet_separation=5):
        """
        These arguments should be helpful in tweaking the outputs to better
        fit the hardware or specific decoder requirements. I.e. if your
        hardware shapes the signal on longer/shorter intervals than the
        actual value, it can be adjusted here.

        Currently only bit_X_part_duration and packet_separation are used.

        Older decoders need a 5ms packet separation. Performance should improve
        by making it 0 if working with new decoders.
        """

        DCCEncoder.__init__(self,
                            bit_one_part_min_duration,
                            bit_one_part_max_duration,
                            bit_one_part_duration,
                            bit_zero_part_min_duration,
                            bit_zero_part_max_duration,
                            bit_zero_part_duration,
                            packet_separation)

        self._string_payload = ""
        self._idle_packet_string = self.idle_packet.to_bit_string()
        self._reset_packet_string = self.reset_packet.to_bit_string()
        self._stop_packet_string = self.stop_packet.to_bit_string()

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, packets):
        self._payload = packets
        bitstrings = map(operator.methodcaller('to_bit_string'),
                         packets)
        self._string_payload = ",".join(bitstrings)

    def send_packet(self, packet, times):
        packet_string = packet.to_bit_string()
        return self.send_bit_string(packet_string + ",", times)

    def send_idle(self, times):
        self.send_bit_string(self._idle_packet_string, times)

    def send_stop(self, times):
        self.send_bit_string(self._stop_packet_string, times)

    def send_reset(self, times):
        self.send_bit_string(self._reset_packet_string, times)

    def send_payload(self, times):
        if len(self._string_payload):
            self.send_bit_string(self._string_payload, times)
            return True
        else:
            return False

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
                                                self.bit_zero_part_duration,
                                                self.packet_separation)

    def tracks_power_on(self):
        return dcc_rpi_encoder_c.brake(0)

    def tracks_power_off(self):
        return dcc_rpi_encoder_c.brake(1)
