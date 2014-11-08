from dcc_encoder import DCCEncoder
from dcc_general_packet import DCCGeneralPacket
import time

class DCCDummyEncoder(DCCEncoder):

    def __init__(self):
        DCCEncoder.__init__(self)

    def send_bit_array(self, bitarray, times):
        packet = DCCGeneralPacket.from_bit_array(bitarray)
        print packet
        print "(%d times...)" % times
        time.sleep(5)
        return True

    def send_bit_arrays(self, bitarray_array, times):
        packets = map(DCCGeneralPacket.from_bit_array, bitarray_array)
        print "----"
        for p in packets:
            print p
        print "---- (%d times...)" % times
        time.sleep(5)
        return True
