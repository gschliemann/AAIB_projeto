from paho.mqtt import client as mqtt_client
import threading
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx
import streamlit as st
import time

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

def on_message(client, userdata, msg):
    print('Message received')
    message = msg.payload.decode()
    st.write(message)

def subscribe():  
    client.subscribe(topic)
    st.write('teste')
    client.on_message = on_message
    print('Subscribing')
    client.loop_forever()

st.title("Microphone Audio Recorder")
st.write(
    "Metrics on how often Pandas is being downloaded from PyPI (Python's main "
    "package repository, i.e. where `pip install pandas` downloads the package from)."
)
col1, col2 = st.columns(2)

with col1:
    if st.button('Record'):
        st.write('Started recording...')

st.write('ola')

client = connect_mqtt()
subscribe()