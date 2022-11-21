import time
import paho.mqtt.client as mqtt
import streamlit as st

def on_connect(client, userdata, flags, rc):
    st.write(f"Connected with result cod to MQTT broker on localhost")

def on_publish(client, userdata, mid):
    print("sent a message")

def on_message(client, userdata, msg):
    print(msg.topic + "  " + str(msg.payload))
    st.write(str(msg.payload.decode('utf-8')))

mqttClient = mqtt.Client()
mqttClient.on_connect = on_connect
mqttClient.on_publish = on_publish
mqttClient.on_message = on_message
mqttClient.connect("mqtt.eclipseprojects.io", 1883, 60)
mqttClient.subscribe("streamlit")
mqttClient.loop_start() # start a new thread

# Why use msg.encode('utf-8') here
# MQTT is a binary based protocol where the control elements are binary bytes and not text strings.
# Topic names, Client ID, Usernames and Passwords are encoded as stream of bytes using UTF-8.
while True:
    msg = "hello"
    info = mqttClient.publish(
        topic='greenhouse/alarm',
        payload=msg.encode('utf-8'),
        qos=0,
    )
    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    print(info.is_published())
    time.sleep(3)