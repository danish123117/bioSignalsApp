import paho.mqtt.client as mqtt
import json 
#import requests 
from ngsiOperations.ngsiv2Operations.ngsiv2CrudOperations import ngsi_get_current
import time 
import numpy as np 

broker_address = "127.0.0.1"
broker_port = 1883
topic = "json/danishabbas1/Robotstate"

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

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")

def CEP_UC1(entityStress):
    time.sleep(5.2)
    indices = np.array([0, 1, 4, 5])
    #client = mqtt.Client()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(broker_address, broker_port, 60)
    client.loop_start()

    try:
        while True:
            start_time = time.time()
            Rob_state = False 
            stress_state = ngsi_get_current(entityStress)
            print(stress_state)
            mean = np.array(stress_state["meanFrequencyState"]['value'])[indices]
            median = np.array(stress_state["medianFrequencyState"]['value'])[indices]
            pow = np.array(stress_state["meanPowerFrequencyState"]['value'])[indices]
            zcf = np.array(stress_state["zeroCrossingFrequencyState"]['value'])[indices]
            cumulative = (pow+ mean) / 2
            Rob_state = not np.any(cumulative > 1)
            payload = json.dumps(mqtt_payload(Rob_state))
            client.publish(topic, payload)
            remaining_time = 5 if not Rob_state else 5
            remaining_time -= time.time() - start_time
            if remaining_time > 0:
                time.sleep(remaining_time)
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) to gracefully disconnect from MQTT broker
        print("Disconnecting from MQTT broker")
        client.disconnect()
        client.loop_stop()

if __name__ == "__main__": 
    CEP_UC1("Stress:005")




            

