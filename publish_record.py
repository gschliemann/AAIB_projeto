from paho.mqtt import client as mqtt_client
import pyaudio
import wave
import numpy as np
import librosa

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

def audio_rec():
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024*8
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "file.wav"
 
    audio = pyaudio.PyAudio()
 
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print ("Recording...")
 
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = np.frombuffer(stream.read(CHUNK),dtype=np.int16)
        S = np.abs(data.astype('float32'))
        publish(S.tobytes())
        #np.append(data)

    print ("Finished recording")
 
 
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    #print(data.size)
    publish('end'.tobytes())

    

 
    #waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    #waveFile.setnchannels(CHANNELS)
    #waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    #waveFile.setframerate(RATE)
    #waveFile.writeframes(b''.join(frames))
    #waveFile.close()

client = connect_mqtt()    

audio_rec()

