class LightSensor:
    def __init__(self, sensor):
        self.sensor = sensor

    def read(self):
        self.sensor.value = 200
        return 200

    def is_dark(self):
        self.read()
        return self.sensor.value < 200