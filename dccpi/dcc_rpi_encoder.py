from dcc_encoder import DCCEncoder
import dcc_rpi_encoder_c
import operator

class DCCRPiEncoder(DCCEncoder):
    """
    Uses a C extension to send the packets quickly.
    """

    def __init__(self,
                 bit_one_part_min_duration=55, #microseconds
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
                            bit_zero_part_max_duraction,
                            bit_zero_part_duration)

    def send_packet(self, packet, times):
        packet_string = packet.to_bit_string()
        return self.send_bit_string(packet_string, times)

    def send_packets(self, packets, times):
        packet_string = "".join(map(operator.methodcaller('to_bit_string'), packets))
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
