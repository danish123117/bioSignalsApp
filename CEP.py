import paho.mqtt.client as mqtt
import json 
import requests 
from ngsiOperations.ngsiv2Operations import ngsi_get_current
import time 
import numpy as np
broker_address = "127.0.0.1"
broker_port = 1883
topic = "Robotstate"
def mqtt_payload(Rob_state):
    current_time = time.strftime("%Y-%m-%dT%H:%M:%S.", time.localtime()) + '{:03d}'.format(int(round(time.time() * 1000)) % 1000)
    payload = {
    "TimeStamp": current_time,
    "automatic": Rob_state
    }
    return payload

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Connection failed with code {rc}")
def stop_trial(client_mqtt):
    client_mqtt.disconnect()
    client_mqtt.loop_stop()

if __name__ == "__main__": 
    time.sleep(5.2)
    indices = [0,1,4,5]
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(broker_address, broker_port, 60)
    client.loop_start()
    while True:
        start_time = time.time()
        Rob_state = False 
        stress_state = ngsi_get_current()
        mean= stress_state["meanFrequencyState"][indices]
        median= stress_state["medianFrequencyState"][indices]
        pow= stress_state["meanPowerFrequencyState"][indices]
        zcf = stress_state["zeroCrossingFrequency"][indices]
        cumulative= (np.array(pow) + np.array(mean))/2
        Rob_state = not np.any(cumulative > 1)
        payload = json.dumps(mqtt_payload(Rob_state))
        client.publish(topic,payload)
        remaining_time = 5 if not Rob_state else 5*60
        remaining_time -= time.time() - start_time
        if remaining_time > 0:
            time.sleep(remaining_time)



            

