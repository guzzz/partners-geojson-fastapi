import os
import pika
import json
import sys
sys.path.append(os.path.realpath('..'))

from app.services.partner_service import PartnerService
from fastapi.encoders import jsonable_encoder
partner_service = PartnerService()


amqp_url: str = os.getenv("AMQP_URL")
params = pika.URLParameters(amqp_url)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue="calculus")

def callback(ch, method, properties, body):
    print("Received in CALCULUS-API")

    data = json.loads(body)
    action = data.get("action")
    body_json = data.get("body")

    if action == "create":
        partner_service.create(body_json)
    elif action == "delete":
        id = body_json.get("id")
        partner_service.delete(id)
    else:
        pass 

channel.basic_consume(queue="calculus", on_message_callback=callback, auto_ack=True)
print("CALCULUS-API queue up!")
channel.start_consuming()
channel.close()
