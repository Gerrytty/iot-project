import time
import board
import adafruit_dht
import psutil
from threading import Thread

class TempSensor(Thread):
    def __init__(self, temp_sensor, humidity_sensor):
        super().__init__()
        self.temp_sensor = temp_sensor
        self.humidity_sensor = humidity_sensor
        for proc in psutil.process_iter():
            if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
                proc.kill()
        self.device = adafruit_dht.DHT11(board.D23)

    def run(self):
        while True:
            try:
                temp = self.device.temperature
                humidity = self.device.humidity
                self.humidity_sensor.value = humidity
                self.temp_sensor.value = temp
                print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
            except RuntimeError as error:
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                sensor.exit()
                raise error
            time.sleep(1.0)

    def read(self):
        temp = self.device.temperature
        humidity = self.device.humidity
        self.humidity_sensor.value = humidity
        self.temp_sensor.value = temp
        return temp, humidity