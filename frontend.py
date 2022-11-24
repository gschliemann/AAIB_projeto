from paho.mqtt import client as mqtt_client
import runpy
import streamlit as st
import time

broker = 'mqtt.eclipseprojects.io'
port = 1883
topic = "AAIB/project"
#topic_sub = "API/notification/#"
# generate client ID with pub prefix randomly
#client_id = 'your client id'
#username = 'your username'
#password = 'your password'
#deviceId = "your deviceId"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)
 
 
    client = mqtt_client.Client()
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, status):
    msg = "Olá"
    result = client.publish(msg,topic)
    msg_status = result[0]
    if msg_status ==0:
        print(f"message : {msg} sent to topic {topic}")
    else:
        print(f"Failed to send message to topic {topic}")

message="n"
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        #print(f"Recieved '{msg.payload.decode()}' from '{msg.topic}' topic")
        #y = json.loads(msg.payload.decode())
        #temp = y["notification"]["parameters"]["temp"]
        #hum = y["notification"]["parameters"]["humi"]
        print(msg.topic+" "+str(msg.payload))
        print("temperature:")
        message = msg.payload.decode()
        

    client.subscribe(topic)
    client.on_message = on_message

client = connect_mqtt()
subscribe(client)

st.title("Microphone Audio Recorder")
st.write(
    "Metrics on how often Pandas is being downloaded from PyPI (Python's main "
    "package repository, i.e. where `pip install pandas` downloads the package from)."
)
col1, col2 = st.columns(2)

with col1:
    if st.button('Record', on_click=publish(client, 0)):
        st.write('Started recording...')

with col2:
    if st.button('Gravar'):
        client.loop_start()
        time.sleep(5)
        client.loop_stop()
        st.write(str(message))


#client.loop_start()

#client.loop_stop()
