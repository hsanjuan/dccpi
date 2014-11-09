from dcc_encoder import DCCEncoder
from dcc_general_packet import DCCGeneralPacket
import time

class DCCDummyEncoder(DCCEncoder):
    """
    This class is meant to easy test that the controller
    is correctly sending packages as it should and print
    the packages to screen... nothing else. It sleeps
    10 secs between packets batch
    """

    SLEEP_BETWEEN_BATCHES=10

    def __init__(self):
        DCCEncoder.__init__(self)

    def send_packet(self, packet, times):
        print packet
        print "(%d times...)" % times
        time.sleep(self.SLEEP_BETWEEN_BATCHES)
        return True

    def send_packets(self, packets, times):
        print "----"
        for p in packets:
            print p
        print "---- (%d times...)" % times
        time.sleep(self.SLEEP_BETWEEN_BATCHES)
        return True
