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
        self.preamble            = BitArray('0b111111111111')
        self.packet_start_bit    = BitArray('0b0')
        self.address_byte        = BitArray(address_byte)
        self.data_byte_start_bit = BitArray('0b0')
        self.data_bytes          = map(BitArray, data_bytes)
        self.packet_end_bit      = BitArray('0b1')

        assert(len(self.address_byte) == 8)
        for byte in self.data_bytes:
            assert(len(byte) == 8)

    def pack(self):
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
        return map(bool, packet)
