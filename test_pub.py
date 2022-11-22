import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import streamlit as st

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("AAIB/project")

# The callback for when a PUBLISH message is received from the server.
def on_publish(client, userdata, msg):
    print("Message sent")

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("mqtt.eclipseprojects.io", 1883, 60)

publish.single("AAIB/project", "boo", hostname="mqtt.eclipseprojects.io")