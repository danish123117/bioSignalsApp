import requests
import json
# generalise this one to take parameters for iD pattern and attributes as inputs. 
def createSubscriptions(entity_name):
    url_t = 'http://localhost:1026/v2/subscriptions/'

    headers_t = {
        'Content-Type': 'application/json',
        'fiware-service': 'openiot',
        'fiware-servicepath': '/'
    }

    operator = {
        "description": "Notify QuantumLeap of change in data of emg sensor data and feaisibility attrs",
        "subject": {
            "entities": [
                {
                    "idPattern": "Sensor.*" 
                }
            ],
            "condition": {
                "attrs": [
                    "TimeStamp" ,
                    "index",
                    "data",
                    "Feaisability"
                    
                ]
            }
        },
        "notification": {
            "http": {
                "url": "http://quantumleap:8668/v2/notify"
            },
            "attrs": [
                    "TimeStamp" ,
                    "index",
                    "data",
                    "Feaisability"
            ],
            "metadata": ["dateCreated", "dateModified"]
        }
    }

    stress = {
        "description": "Notify QuantumLeap of change in data of extracted stress features",
        "subject": {
            "entities": [
                {
                    "idPattern": "Stress.*" 
                }
            ],
            "condition": {
                "attrs": [
                    "medianFrequencyState" ,
                    "meanFrequencyState",
                    "meanPowerFrequencyState",
                    "zeroCrossingFrequencyState"
                                
                ]
            }
        },
        "notification": {
            "http": {
                "url": "http://quantumleap:8668/v2/notify"
            },
            "attrs": [
                    "medianFrequencyState" ,
                    "meanFrequencyState",
                    "meanPowerFrequencyState",
                    "zeroCrossingFrequencyState"
            ],
            "metadata": ["dateCreated", "dateModified"]
        }
    }

    subscription_operator_response= requests.post(url_t, headers=headers_t, data=json.dumps(operator))
    subscription_stress_response = requests.post(url_t, headers=headers_t, data=json.dumps(stress))
    return subscription_operator_response, subscription_stress_response
