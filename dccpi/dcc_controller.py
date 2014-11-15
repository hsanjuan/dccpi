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

import threading
from dcc_baseline_packet_factory import DCCBaselinePacketFactory


class DCCController(object):
    """
    A DCC controller take care of generating the packages and sending
    them using a DCCEncoder of choice.

    It allows to register DCCLocomotives and runs a separate thread
    to send them packages.
    """

    def __init__(self, dcc_encoder):
        """
        Initialize the controller. We need to have an encoder instance for that
        """
        self.dcc_encoder = dcc_encoder
        self.state = 'idle'
        self.devices = {}
        self._thread = None

    def register(self, dcc_device):
        self.devices[dcc_device.name] = dcc_device

    def unregister(self, dcc_device):
        if type(dcc_device) is str:
            del self.devices[dcc_device]
        else:
            del self.devices[dcc_device.name]

    def start(self):
        if self._thread:
            print("Controller already running")
            return None
        self._thread = DCCControllerThread(self)
        self.state = 'startup'
        self._thread.start()

    def stop(self):
        self.state = 'shutdown'
        self._thread.join()
        self._thread = None


class DCCControllerThread(threading.Thread):
    """
    Runs the thread.

    It uses a small state machine to control state:
      * Startup: broadcast reset packet
      * Run: send packets to devices
      * Shutdown: broadcast stop packet
      * Idle: send idle packets
    """
    def __init__(self,
                 dcc_controller):
        self.dcc_controller = dcc_controller
        self.dcc_encoder = dcc_controller.dcc_encoder

        # Shorthands
        self.idle_packet = DCCBaselinePacketFactory.idle_packet()
        self.reset_packet = DCCBaselinePacketFactory.reset_packet()
        self.stop_packet = DCCBaselinePacketFactory.stop_packet()
        threading.Thread.__init__(self)

    def run(self):
        while(True):
            state = self.dcc_controller.state
            if state is 'idle':
                self.dcc_encoder.send_packet(self.idle_packet, 20)
            elif state is 'startup':
                self.dcc_encoder.send_packet(self.reset_packet, 20)
                self.dcc_controller.state = 'run'
            elif state is 'shutdown':
                self.dcc_encoder.send_packet(self.stop_packet, 20)
                self.dcc_encoder.send_packet(self.reset_packet, 20)
                break
            elif state is 'run':
                packets = []
                for name, device in self.dcc_controller.devices.iteritems():
                    packets.append(device.control_packet())
                self.dcc_encoder.send_packets(packets, 10)
            else:
                print "unknown state"
                break
