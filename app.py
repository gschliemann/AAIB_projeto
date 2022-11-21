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

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    st.write(str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt.eclipseprojects.io", 1883, 60)
client.loop_start() # start a new thread
client.subscribe("streamlit")

while True:
    try:
        time.sleep(1)
                
    except:
        continue
    