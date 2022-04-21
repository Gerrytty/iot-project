import json
from types import SimpleNamespace


class AlarmTime:
    def __init__(self, time_to_alarm):
        self.time_to_alarm = time_to_alarm

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    @staticmethod
    def to_class(json_string):
        return json.loads(json_string, object_hook=lambda d: SimpleNamespace(**d))