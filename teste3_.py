import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import streamlit as st
from threading import Thread
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.runtime.scriptrunner import add_script_run_ctx
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("AAIB/project")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    st.write(msg.payload.decode())
    
def target():
    st.write("msg.payload.decode()")

t = Thread(target=target)
add_script_run_ctx(t)
t.start()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipseprojects.io", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()
#client.loop_start()

publish.single("AAIB/project", "boo", hostname="mqtt.eclipseprojects.io")
time.sleep(3)
