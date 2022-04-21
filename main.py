from mqtt_producer import MQTTProducer

if __name__ == "__main__":
    producer1 = MQTTProducer("broker.hivemq.com", 1883, "producer")
    producer1.produce("itis/team1/sensors123", "Hello")