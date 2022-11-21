import paho.mqtt.client as mqtt

import streamlit as st
import time

MQTT_BROKER = 'localhost'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    st.write(f"Connected with result code {str(rc)} to MQTT broker on {MQTT_BROKER}")

def on_disconnect(client, userdata,rc=0):
    print("DisConnected result code "+str(rc))
    client.loop_stop()

def on_publish(client, userdata, mid):
    print("sent a message")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    st.write(msg.payload.decode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message
client.connect("mqtt.eclipseprojects.io", 1883, 60)
client.subscribe("streamlit")

client.loop_start()

while True:
    msg = "hello"
    info = client.publish(
        topic='greenhouse/alarm',
        payload=msg.encode('utf-8'),
        qos=0,
    )
    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)




    