from paho.mqtt import client as mqtt_client
from random import randint
import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS

load_dotenv()  # take environment variables from .env.

# InfluxDB config
BUCKET = os.getenv('INFLUXDB_BUCKET')
db_client = InfluxDBClient(url=os.getenv('INFLUXDB_URL'),
                token=os.getenv('INFLUXDB_TOKEN'), org=os.getenv('INFLUXDB_ORG'))
write_api = db_client.write_api()
MQTT_PUBLISH_TOPIC = "emqx/esp8266_lab_jk_pd"


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("emqx/esp8266_lab_jk_pd")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    measurement = int(msg.payload)

    ## InfluxDB logic
    point = Point(MQTT_PUBLISH_TOPIC).tag("temperature").field("temperature", measurement )
    write_api.write(bucket=BUCKET, record=point)

client_id = f'python-mqtt-{randint(0, 1000)}'
client = mqtt_client.Client(client_id)
client.tls_set(ca_certs='./broker.emqx.io-ca.crt')
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.emqx.io", 8883)

client.loop_forever()
print(f"Received the following message: {client.user_data_get()}")