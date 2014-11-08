class DCCLocomotive(object):
    """
    A locomotive is a thing with speed, direction and lights
    """
    def __init__(self,
                 name,
                 address,
                 speed = 0,
                 direction = 1,
                 headlight_on=False,
                 headlight_support=True):
        self.name = name
        self.speed = speed
        self.address = address
        self.direction = direction
        self.headlight_on = headlight_on,
        self.headlight_support = headlight_support

    def emergency_stop(self):
        self.speed = 1

    def stop(self):
        self.speed = 0

    def reverse(self):
        self.direction = 0 if (self.direction) else 1

    def turn_headlight_on(self):
        self.headlight_on = True

    def turn_headlight_off(self):
        self.headlight_on = False

    def switch_headlight(self):
        self.headlight = False if (self.headlight) else True

    def slower(self):
        # Skip emergency stop
        if self.speed is 2:
            self.set_speed(0)
        else:
            self.set_speed(self.speed - 1)

    def faster(self):
        if self.speed is 0:
            self.set_speed(2)
        else:
            self.set_speed(self.speed + 1)

    def set_speed(self, speed):
        # Make some basic checks
        speed = abs(speed)
        if self.headlight_support:
            self.speed = min(15, speed)
        else:
            self.speed = min(31, speed)
    
