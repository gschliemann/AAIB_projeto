from paho.mqtt import client as mqtt_client
import threading
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx
import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt

#MQTT configuration

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
    message = msg.payload.decode('latin-1').encode("utf-8")
    np_message = np.frombuffer(message,dtype=np.int16)
    #st.pyplot(np_message)

def subscribe():  
    client.subscribe(topic)
    client.on_message = on_message
    print('Subscribing')
    client.loop_forever()

client = connect_mqtt()

#Streamlit Frontend

st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)

st.title("Real-Time Audio Recorder using Paho MQTT")
st.write(
    'This is a project developed for the subject of AIIB at FCT-UNL'
)
col1, col2 = st.columns(2)

with col1:
    if st.button('Record'):
        st.write('Started recording...')
        for seconds in range(200):
            if 'mqttThread' not in st.session_state:
                st.session_state.mqttThread = threading.Thread(target=subscribe)
                add_script_run_ctx(st.session_state.mqttThread)
                st.session_state.mqttThread.start()
                print('Thread is working')
    
            time.sleep(1)
