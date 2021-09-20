import os
import pika
import json

from fastapi.encoders import jsonable_encoder
from shapely.validation import explain_validity, make_valid
from shapely.geometry import mapping
from marshmallow_geojson import GeoJSONSchema
from app.utils.geojson_converter import geojson2shp

geojson_schema = GeoJSONSchema()


amqp_url: str = os.getenv("AMQP_URL")
params = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(action, body={}, partner_id=None):
    print("==> Sending from PARTNERS-API")
    try:
        if action == "create":
            partner = jsonable_encoder(body)
            geojson = partner.get("coverageArea")
            need_fix = geojson.get("Self-intersection", False)
            if need_fix:
                print("Adapting Self-intersection in Multipolygon for calculus API")  
                del geojson["Self-intersection"]
                shapely_obj = geojson2shp(geojson)
                valid_shape = make_valid(shapely_obj)
                valid_shape_json = mapping(valid_shape)
                partner["coverageArea"] = valid_shape_json

            data = {}
            data["action"] = action
            data["body"] = partner
            data["partner_id"] = partner_id
        
        elif action == "delete":
            data = {}
            data["action"] = action
            data["body"] = body

        properties = pika.BasicProperties(content_type="application/json")
        channel.basic_publish(exchange="", routing_key="calculus", body=json.dumps(data), properties=properties)
    except Exception as exc:
        print(f"==> ERROR: {exc} - Please restart queue link")
