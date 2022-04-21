from sensor import Sensor
from kafka_producer import KafkaProducer
from light_sensor import LightSensor
import time
from alarm import Alarm
from led import Led
import json
from temp_sensor import TempSensor

from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread


# sensor initialization
temp_and_humidity_sensor = TempSensor(Sensor(0, "temp sensor", 0), Sensor(1, "humidity sensor", 0))
temp_and_humidity_sensor.start()
led_sensor = Led(Sensor(1, "led", 0))


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        global temp_and_humidity_sensor
        if self.path == "/sensors/temp":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(f"{temp_and_humidity_sensor.temp_sensor.value}\n", "utf-8"))
        elif self.path == "/sensors/humidity":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(f"{temp_and_humidity_sensor.humidity_sensor.value}\n", "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


class Serv(Thread):
    def __init__(self, hostName, serverPort):
        super().__init__()
        self.webServer = HTTPServer((hostName, serverPort), MyServer)
        print("Server started http://%s:%s" % (hostName, serverPort))

    def run(self) -> None:
        try:
            self.webServer.serve_forever()
        except KeyboardInterrupt:
            self.join()
            self.webServer.server_close()
            print("Server stopped.")


if __name__ == "__main__":

    hostName = "192.168.88.42"
    serverPort = 8030
    serv = Serv(hostName, serverPort)
    serv.start()

    # main logic in alarm
    alarm = Alarm("12:00", led_sensor)
    alarm.start_alarm()

    # producer
    producer = KafkaProducer("192.168.88.241:9092")

    arr = [temp_and_humidity_sensor.temp_sensor, temp_and_humidity_sensor.humidity_sensor]

    while True:
        try:
            # send message to kafka broker
            producer.produce([json.dumps([ob.__dict__ for ob in arr])], "sensors")
            time.sleep(1)
        except KeyboardInterrupt:
            print("STOP all")
            alarm.stop()
            led_sensor.off()
            break
