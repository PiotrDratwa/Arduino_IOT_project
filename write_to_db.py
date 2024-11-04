from paho.mqtt import client as mqtt_client
from random import randint

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("emqx/esp8266_lab_jk_pd")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client_id = f'python-mqtt-{randint(0, 1000)}'
client = mqtt_client.Client(client_id)
client.tls_set(ca_certs='./broker.emqx.io-ca.crt')
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.emqx.io", 8883)

client.loop_forever()
print(f"Received the following message: {client.user_data_get()}")