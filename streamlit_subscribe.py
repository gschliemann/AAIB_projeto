from paho.mqtt import client as mqtt_client
import threading
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx
import streamlit as st
import time
import numpy as np
import matplotlib.pyplot as plt
import csv

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

data = []
def on_message(client, userdata, msg):
    message = msg.payload.decode('unicode-escape').encode('ISO-8859-1')
    np_message = np.frombuffer(message,dtype=np.float64) 
    with placeholder2.container():
        st.write('Started recording...')
        display(np_message)
        data.append(np_message.tolist())
    
    
def subscribe():  
    client.subscribe(topic)
    client.on_message = on_message
    print('Subscribing')
    client.loop_forever()

def display(data):
    fig, ax = plt.subplots()
    ax.plot(data)
    st.pyplot(fig)
    plt.close(fig)

def mqtt_thread():
    for seconds in range(15):
            if 'mqttThread' not in st.session_state:
                st.session_state.mqttThread = threading.Thread(target=subscribe)
                add_script_run_ctx(st.session_state.mqttThread)
                st.session_state.mqttThread.start()
    
            time.sleep(1)
    
    del st.session_state['mqttThread']


def convert_df(data_):
    with open('shows.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows(data_)
    return f

client = connect_mqtt()

#Streamlit Frontend

st.title("Real-Time Audio Recorder using Paho MQTT")
st.write(
    'This is a project developed for the subject of AIIB at FCT-UNL'
)

placeholder = st.empty()

with placeholder.container():

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Record', key='rec'):
            placeholder2 = st.empty()
            mqtt_thread()

    with col2:
        if st.button('Download', key='down'):
            st.write(data)
        #st.download_button(
            #label="Download",
            #data=convert_df(data),
            #file_name='large_df.csv',
            #mime='text/csv',
        #) 