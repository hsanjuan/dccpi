from dcc_baseline_packet_factory import DCCBaselinePacketFactory
import threading

class DCCController(object):
    """
    A DCC controller is used to send DCC packets to the tracks.

    It works by registering locos and then it will continously send
    packets addressed to the registered locos using a separate thread.

    """

    def __init__(self,
                 dcc_encoder):
        """
        dcc_encoder is the class that sends the signals to the track
        given a package
        """
        self.dcc_encoder = dcc_encoder
        self.state = 'idle'
        self.devices = {}
        self._thread  = DCCControllerThread(self)

    def register(self, dcc_device):
        self.devices[dcc_device.name] = dcc_device

    def unregister(self, dcc_device):
        if type(dcc_device) is str:
            del self.devices[dcc_device]
        else:
            del self.devices[dcc_device.name]

    def start(self):
        self.state = 'startup'
        self._thread.start()

    def stop(self):
        self.state = 'shutdown'
        self._thread.join()


class DCCControllerThread(threading.Thread):
    """
    Runs the thread.

    It uses a small state machine to control state:
    Idle -> Startup -> Run -> Shutdown -> Idle
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
                factory = DCCBaselinePacketFactory
                for name,device in self.dcc_controller.devices.iteritems():
                    p = factory.speed_and_direction_packet(device.address,
                                                           device.speed,
                                                           device.headlight_on,
                                                           device.direction,
                                                           device.headlight_support)
                    packets.append(p)
                self.dcc_encoder.send_packets(packets, 10)
            else:
                print "unknown state"
                break
