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

import time
import threading
import sys
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
        self._state = 'idle'
        self.devices = {}
        self._thread = None
        self.devices_lock = threading.Lock()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new):
        if self._state != new:
            print("New state is %s" % new)
            self._state = new

    def register(self, dcc_device):
        dcc_device.notify_update_callback = self.update_payload
        self.devices[dcc_device.name] = dcc_device
        print("%s registered on address #%s" % (dcc_device.name,
                                                dcc_device.address))
        self.update_payload()

    def unregister(self, dcc_device):
        if type(dcc_device) is str:
            del self.devices[dcc_device]
        else:
            del self.devices[dcc_device.name]
        print("%s has been unregistered" % dcc_device.name)
        self.update_payload()

    def update_payload(self, device_name='*'):
        t0 = time.clock()
        packets = []
        for name, device in self.devices.iteritems():
            packets.append(device.control_packet())
        self.dcc_encoder.payload = packets
        t1 = time.clock()
        print("DCC payload updated (in %f seconds)" % (t1 - t0))
        if self._thread:
            self.state = 'active'

    def start(self):
        if self._thread:
            print("DCC Controller already running")
            return None
        print("Starting DCC Controller")
        self._thread = DCCControllerThread(self)
        self.state = 'startup'
        self._thread.start()

    def stop(self):
        self.state = 'shutdown'
        self._thread.join()
        self._thread = None
        print("DCC Controller stopped")


class DCCControllerThread(threading.Thread):
    """
    Runs the thread.

    It uses a small state machine to control state:
      * Startup: broadcast reset packet
      * Active: send control packets payload
      * Shutdown: broadcast stop packet
      * Idle: send idle packets
    """
    def __init__(self,
                 dcc_controller):
        self.dcc_controller = dcc_controller
        self.dcc_encoder = dcc_controller.dcc_encoder

        # Let's have these ready
        self.idle_packet = DCCBaselinePacketFactory.idle_packet()
        self.reset_packet = DCCBaselinePacketFactory.reset_packet()
        self.stop_packet = DCCBaselinePacketFactory.stop_packet()
        threading.Thread.__init__(self)

    def run(self):
        while(True):
            state = self.dcc_controller.state
            if state is 'idle':
                self.dcc_encoder.send_packet(self.idle_packet, 10)
            elif state is 'startup':
                self.dcc_encoder.tracks_power_on()
                self.dcc_encoder.send_packet(self.reset_packet, 10)
                self.dcc_controller.state = 'active'
            elif state is 'shutdown':
                self.dcc_encoder.send_packet(self.stop_packet, 10)
                self.dcc_encoder.send_packet(self.reset_packet, 10)
                self.dcc_encoder.tracks_power_off()
                break
            elif state is 'active':
                result = self.dcc_encoder.send_payload(10)
                if not result:  # empty payload perhaps
                    self.dcc_controller.state = 'idle'
                else:
                    # The main controller thread needs time to
                    # perform (perhaps) payload updates
                    time.sleep(0.015)
            else:
                sys.stderr.write("Unknown state %s!" % state)
                break
