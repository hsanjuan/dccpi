NRMA Digical Command Control (DCC) implementation for Raspberry Pi
==================================================================

This module allows to use a minimal subset of the DCC protocol to
control DCC-compatible devices, usually model trains, using the 
Raspberry PI GPIO interface.

It is based on the:
  * [S-91 Electrical Standard](http://www.nmra.org/sites/default/files/standards/sandrp/pdf/s-9.1_electrical_standards_2006.pdf)
  * [S-92 DCC Communications Standard](http://www.nmra.org/sites/default/files/s-92-2004-07.pdf)

Example with dummy encoder
--------------------------

    import dccpi

    controller = DCCController(DCCDummyEncoder())
    loco1 = DCCLocomotive(name="my loco", address=3, speed=0)
    controller.register(loco1)
    controller.start()
    # The encoder sends the packets on a different thread
    loco.faster()
    # ...
    loco.stop()
    controller.stop()
