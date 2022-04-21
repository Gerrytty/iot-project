import json
from types import SimpleNamespace


class Sensor:
    def __init__(self, sensor_id, type_sensor, value):
        self.sensorID = sensor_id
        self.typeSensor = type_sensor
        self.value = value

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    @staticmethod
    def to_class(json_string):
        return json.loads(json_string, object_hook=lambda d: SimpleNamespace(**d))

