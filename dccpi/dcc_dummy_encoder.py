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
import time


class DCCDummyEncoder(DCCEncoder):
    """
    This class is meant to easy test that the controller
    is correctly sending packages as it should and print
    the packages to screen... nothing else. It sleeps
    10 secs between packets batch
    """

    SLEEP_BETWEEN_BATCHES = 10

    def __init__(self):
        DCCEncoder.__init__(self)

    def send_packet(self, packet, times):
        print(packet)
        print("(%d times...)" % times)
        time.sleep(self.SLEEP_BETWEEN_BATCHES)
        return True

    def send_payload(self, times):
        if not len(self.payload):
            return False
        print("----")
        for p in self.payload:
            print(p)
        print("---- (%d times...)" % times)
        time.sleep(self.SLEEP_BETWEEN_BATCHES)
        return True
