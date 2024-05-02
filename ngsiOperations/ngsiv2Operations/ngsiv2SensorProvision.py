import requests

def sensor_provision(sensor_entity,api_key='placeholder_api_key'):
# provision service path
    url = 'http://localhost:4041/iot/services'
    headers = {
        'Content-Type': 'application/json',
        'fiware-service': 'openiot',
        'fiware-servicepath': '/'
    }
    data = {
        "services": [
            {
                "apikey": "danishabbas",
                "cbroker": "http://orion:1026",
                "entity_type": "Thing",
                "resource": "/iot/json"
            }
        ]
    }

    servicepath_provision_response = requests.post(url, json=data, headers=headers)
    #print(servicepath_response.status_code)
    #print(servicepath_response.text)
    #provision EMG sensor
    url = 'http://localhost:4041/iot/devices'
    headers = {
        'Content-Type': 'application/json',
        'fiware-service': 'openiot',
        'fiware-servicepath': '/'
    }
    data = {
        "devices": [
            {
                "device_id": "EMG1000",
                "entity_name": sensor_entity,
                "entity_type": "Sensor",
                "transport":   "MQTT",
                "timezone": "Europe/Berlin",
                "attributes": [
                    {"object_id": "TimeStamp", "name": "TimeStamp", "type": "Text"},
                    {"object_id": "data", "name": "data", "type": "array"},
                    {"object_id": "index", "name": "index", "type": "Integer"},
                    {"object_id": "Feaisability", "name": "Feaisability", "type": "array"}
                    
                ]

            }
        ]
    }
    sensor_provision_response = requests.post(url, json=data, headers=headers)
    #print(sensor_response.status_code)
    #print(sensor_response.text)
    return servicepath_provision_response , sensor_provision_response
