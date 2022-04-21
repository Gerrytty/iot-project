from confluent_kafka.admin import AdminClient
from confluent_kafka import Producer


class KafkaProducer:
    def __init__(self, bootstrap_server):
        self.bootstrap_server = bootstrap_server
        self.admin_client = AdminClient({'bootstrap.servers': bootstrap_server})
        self.producer = Producer({'bootstrap.servers': bootstrap_server})

    def produce(self, source_data, topic):
        def delivery_report(err, msg):
            if err is not None:
                print(f'Message delivery failed: {err}')
            else:
                message_string = msg.value().decode("utf-8")
                print(f'Message delivered: "{message_string}" to {msg.topic()} [partition {msg.partition()}]')

        for data in source_data:
            self.producer.poll(0)
            self.producer.produce(topic, data.encode('utf-8'), callback=delivery_report)

        r = self.producer.flush(timeout=5)
        if r > 0:
            print(f'Message delivery failed ({r} message(s) still remain, did we timeout sending perhaps?)\n')

    def send_msg(self, msg, topic_name):
        try:
            self.produce([msg], topic_name)
        except Exception:
            return "fail"
        return "ok"
