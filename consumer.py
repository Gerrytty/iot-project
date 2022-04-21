from kafka import KafkaConsumer
import json
from threading import Thread


class SensorsUpdater:
    def __init__(self, topic_name, bootstrap_servers):
        self.arr_of_vals_of_sensor = []
        self.arr_of_vals_of_sensor_humidity = []
        self.consumer = KafkaConsumer(topic_name, bootstrap_servers=bootstrap_servers)
        self.stop = False

    def consume_and_update(self):
        while not self.stop:
            for message in self.consumer:
                print(message)
                msg = json.loads(message.value.decode("utf-8"))
                for sensor in msg:
                    if sensor["sensorID"] == 0:
                        self.arr_of_vals_of_sensor.append(sensor["value"])
                    elif sensor["sensorID"] == 1:
                        self.arr_of_vals_of_sensor_humidity.append(sensor["value"])

    def endless_consume(self):
        new_thread = Thread(target=self.consume_and_update)
        new_thread.start()