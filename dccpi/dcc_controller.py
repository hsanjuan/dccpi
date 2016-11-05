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

import time
import threading
import sys


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
        self._abort = False
        self.devices = {}
        self._thread = None
        self.devices_lock = threading.Lock()

    def __str__(self):
        "DCC Controller. %i locos managed" % self.devices.keys()

    def __repr__(self):
        str = "DCC Controller:\n"
        str += "-----------------------------"
        if sys.version_info.major < 3:
            items = self.devices.iteritems()
        else:
            items = self.devices.items()
        for n, device in items:
            str += device.__repr__()
            str += "-----------------------------"
        return str

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new):
        if self._state != new:
            # print("New state is %s" % new)
            self._state = new

    def register(self, dcc_device):
        dcc_device.notify_update_callback = self.update_payload
        self.devices[dcc_device.name] = dcc_device
        print("%s registered on address #%s" % (dcc_device.name,
                                                dcc_device.address))
        self.update_payload()

    def unregister(self, dcc_device):
        if type(dcc_device) is str:
            self.devices[dcc_device].notify_update_callback = None
            del self.devices[dcc_device]
        else:
            del self.devices[dcc_device.name]
            dcc_device.notify_update_callback = None
        print("%s has been unregistered" % dcc_device.name)
        self.update_payload()

    def update_payload(self, device_name='*'):
        # t0 = time.clock()
        packets = []

        if sys.version_info.major < 3:
            items = self.devices.iteritems()
        else:
            items = self.devices.items()

        for name, device in self.devices.items():
            packets += device.control_packets()

        # FIXME: Thread unsafe! What if we write while reading?
        self.dcc_encoder.payload = packets
        # t1 = time.clock()
        # print("DCC payload updated (in %f seconds)" % (t1 - t0))

        # The state machine will come to the new payload state
        # eventually
        #if self._thread:
        #    # FIXME: Thread unsafe! While if we write while writing?
        #self.state = 'newpayload'

    def start(self):
        if self._thread:
            print("DCC Controller already running")
            return None
        print("Starting DCC Controller")
        self._thread = DCCControllerThread(self)
        self._abort = False
        self.state = 'startup'
        self._thread.start()

    def stop(self):
        self._abort = True
        if self._thread:
            self._thread.join()
            self._thread = None
            print("DCC Controller stopped")
        else:
            print("DCC Controller not running")


class DCCControllerThread(threading.Thread):
    """
    Runs the thread.

    It uses a small state machine to control state:
      * Startup: broadcast reset packet
      * New payload: send control packets payload
      * Shutdown: broadcast stop packet
      * Idle: send idle packets
    """
    def __init__(self,
                 dcc_controller):
        self.dcc_controller = dcc_controller
        self.dcc_encoder = dcc_controller.dcc_encoder
        threading.Thread.__init__(self)

    def run(self):
        # We can play a bunch of variables here:
        # How many payload packets do we send?
        # How many idle packages do we send?
        # How long do we sleep? We NEED to sleep because otherwise
        # the thread becomes very unresponsive
        try:
            idle_count = 0
            while(True):
                state = self.dcc_controller.state
                abort = self.dcc_controller._abort
                if abort:
                    state = 'shutdown'

                if state is 'idle':
                    self.dcc_encoder.send_idle(1)
                    idle_count += 1
                    if idle_count >= 1: # Disable idles for the moment
                        self.dcc_controller.state = 'newpayload'
                elif state is 'startup':
                    self.dcc_encoder.tracks_power_on()
                    self.dcc_encoder.send_reset(2)
                    self.dcc_controller.state = 'newpayload'
                elif state is 'shutdown':
                    self.dcc_encoder.send_stop(2)
                    self.dcc_encoder.send_reset(2)
                    self.dcc_encoder.tracks_power_off()
                    break
                elif state is 'newpayload':
                    self.dcc_encoder.send_payload(15)
                    self.dcc_controller.state = 'idle'
                    idle_count = 0
                else:
                    sys.stderr.write("Unknown state %s!" % state)
                    self.dcc_controller.state = 'shutdown'

                time.sleep(0.008)
        except:
            self.dcc_encoder.tracks_power_off()
            m = "An exception ocurred! Please stop the controller!"
            sys.stderr.write(m)
            raise
