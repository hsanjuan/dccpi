from bitstring import BitArray
from dcc_general_packet import DCCGeneralPacket

class DCCBaselinePacket(DCCGeneralPacket):
    """
    DCC Package Type for minimal interoperability
    """
    def __init__(self,
                 address,
                 speed,
                 direction=0):
        """
        Given an address and an instruction, we can construct a general
        packet.

        param address int is the dcc device address
        param speed   int is the speed:
            * 0 - Stop
            * 1 - Stop (I)
            * 2 - E-Stop
            * 3 - E-Stop (I)
            * 4..31 - Step 1..Step 20
        param direction int is 1 for forward and 0 for backwards
        """
        address_bin = BitArray('uint:8=%d' % address)
        instruction_bin = BitArray('0b01')
        if direction:
            instruction_bin.append('0b1')
        else:
            instruction_bin.append('0b0')
        # According to the Standard, speed is 5 bits
        # We rorate it so that the C-bit (the 5th)
        # is in the right position
        speed_bin = BitArray('uint:5=%d' % speed)
        speed_bin.ror(1)
        instruction_bin.append(speed_bin)
        error = address_bin ^ instruction_bin

        data = [ instruction_bin, error ]
        DCCGeneralPacket.__init__(self, hex(address), data)
