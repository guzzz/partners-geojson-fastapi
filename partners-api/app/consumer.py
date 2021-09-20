import os
import pika
import json


amqp_url: str = os.getenv("AMQP_URL")
params = pika.URLParameters(amqp_url)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue="partners")


def callback(ch, method, properties, body):
    print("Received in PARTNERS-API")
    data = json.loads(body)

channel.basic_consume(queue="partners", on_message_callback=callback, auto_ack=True)
print("PARTNERS-API queue up!")
channel.start_consuming()
channel.close()
