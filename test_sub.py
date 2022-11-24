import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import streamlit as st
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("AAIB/project")

message="n"
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    message = msg.payload.decode()
    time.sleep(10)
    st.write(message)
    print(message)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt.eclipseprojects.io", 1883, 60)

st.title("Microphone Audio Recorder")
st.write(
    "Metrics on how often Pandas is being downloaded from PyPI (Python's main "
    "package repository, i.e. where `pip install pandas` downloads the package from)."
)
col1, col2 = st.columns(2)

with col1:
    if st.button('Record'):
        st.write('Started recording...')

with col2:
    if st.button('Gravar'):
        client.loop_start()
        time.sleep(5)
        client.loop_stop()
        st.write(str(message))

#client.loop_forever()
#client.loop_start()
#time.sleep(10)
#client.loop_stop()