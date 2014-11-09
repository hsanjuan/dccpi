import operator
import sys

class DCCEncoder(object):
    """
    A DCC encoder takes a packet or packets and encodes them into the DCC protocol
    electrical standard.

    This class is meant to be extended by subclasses that implement
    the relevant methods to actually send the bits (a dummy output would only
    print it in screen, a RPI class would use GPIO to send them)
    """
    MICROSECOND_DIV=1000000.0

    def __init__(self,
                 bit_one_part_min_duration=55, #microseconds
                 bit_one_part_max_duration=61,
                 bit_one_part_duration=58,
                 bit_zero_part_min_duration=95,
                 bit_zero_part_max_duraction=9900,
                 bit_zero_part_duration=100):
        self.bit_one_part_min_duration = bit_one_part_min_duration
        self.bit_one_part_max_duration = bit_one_part_max_duration
        self.bit_one_part_duration = bit_one_part_duration
        self.bit_zero_part_min_duration = bit_zero_part_min_duration
        self.bit_zero_part_max_duraction = bit_zero_part_max_duraction
        self.bit_zero_part_duration = bit_zero_part_duration

    def send_packet(self, packet, times):
        # to be implemented by subclass
        sys.stderr.write("send_packet() not implemented!")
        return False

    def send_packets(self, packets, times):
        # to be implemented by subclass
        sys.stderr.write("send_packets() not implemented!")
        return False
