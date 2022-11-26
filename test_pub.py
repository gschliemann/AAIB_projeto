from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as publ
import streamlit as st

broker = 'mqtt.eclipseprojects.io'
port = 1883
topic = "AAIB/project"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish():
    msg = "ola"
    publ.single(topic, msg, hostname=broker)
    result = client.publish(msg,topic)
    msg_status = result[0]
    if msg_status ==0:
        print(f"Message sent to topic {topic}")
    else:
        print(f"Failed to send message to topic {topic}")

client = connect_mqtt()

publish()