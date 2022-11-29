from paho.mqtt import client as mqtt_client
import pyaudio
import wave
import numpy as np
import librosa
import threading
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

def publish(msg):
    result = client.publish(topic,msg)
    msg_status = result[0]
    if msg_status ==0:
        print(f"Message sent to topic {topic}")
    else:
        print(f"Failed to send message to topic {topic}")

def on_message(client, userdata, msg):
    if str(msg.payload.decode('latin1')) == 'Start':
        audio_rec()
        
def subscribe():  
    client.subscribe(topic)
    client.on_message = on_message
    client.loop_forever()

def audio_rec():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 22050
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "file.wav"
 
    audio = pyaudio.PyAudio()
 
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print ("Recording...")
    
    frames=[]
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        #data = stream.read(CHUNK)
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        frames.append(data)
        #S = np.abs(data.astype('float32'))
        #publish(S.tobytes())
        #np.append(data)

    print ("Finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    #print(frames)
    y = np.array(frames)
    print(np.shape(y))
    S = np.abs(librosa.stft(y.astype('float32'), n_fft=512))
    print(np.shape(S))
    publish(str(S.tolist()))
    #print(data.size)
    #publish('end'.tobytes())

    #waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    #waveFile.setnchannels(CHANNELS)
    #waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    #waveFile.setframerate(RATE)
    #waveFile.writeframes(b''.join(frames))
    #waveFile.close()

client = connect_mqtt()  

sub=threading.Thread(target=subscribe)
pub=threading.Thread(target=publish, args=(1,))
sub.start()