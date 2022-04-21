from sensor import Sensor
from kafka_producer import KafkaProducer
from light_sensor import LightSensor
import time
from alarm import Alarm
from led import Led
import json


if __name__ == "__main__":

    # sensor initialization
    light_sensor = LightSensor(Sensor(0, "light sensor", 200))
    led_sensor = Led(Sensor(1, "led", 1))

    # main logic in alarm
    alarm = Alarm("15:48", light_sensor, led_sensor)
    alarm.start_alarm()

    # producer
    producer = KafkaProducer("192.168.88.241:9092")

    arr = [led_sensor.led, led_sensor.led]

    while True:
        try:
            # send message to kafka broker
            arr = [led_sensor.led, led_sensor.led]
            # producer.produce([json.dumps([ob.__dict__ for ob in arr])], "topic_1")
            time.sleep(1)
        except KeyboardInterrupt:
            alarm.stop()
            break
