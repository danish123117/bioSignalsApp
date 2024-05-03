import requests
def stress_payload(frequency_median_norm, frequency_mean_norm, frequency_meanPower_norm, frequency_zeroCrossing_norm):
    payload_raw = {
        "medianFrequencyState": {
        "type": "array",
        "value": frequency_median_norm},
        "meanFrequencyState": {
         "type": "array",
         "value": frequency_mean_norm },
       "meanPowerFrequencyState": {
          "type": "array",
          "value": frequency_meanPower_norm
        },
        "zeroCrossingFrequencyState": {
          "type": "array",
          "value": frequency_zeroCrossing_norm
        },
     }
    return payload_raw

def ngsi_get_historical(entity, window_length=5000, url="localhost:8668" , attribute = "data"): 
    """
    The function queries historical data from crateDB using quantum leap API 
    """
    url = f"http://{url}/v2/entities/{entity}/attrs/{attribute}"
    payload ={}
    headers = {
        'fiware-service': 'openiot',
        'fiware-servicepath': '/'
 #       'Content-Type':"application/json"
        }
    params = {
        'lastN': window_length
        }
    response = requests.request("GET",url, headers=headers, params=params,data= payload)
   # if response.status_code == 200:
    return response.json()

def ngsi_patch(payload,entity,entity_type='Stress',url ="localhost:1026"):
    """
    The function update the value on an NGSI entity using patch to orion context broker
    """
    url_f = f"http://{url}/v2/entities/{entity}/attrs/?type={entity_type}"
  #  url = f'http://localhost:1026/v2/entities/' + entity +'/attrs?type=Stress'
    headers = {
        'Content-Type':"application/json"
  #      'fiware-service': 'openiot',
  #      'fiware-servicepath': '/'
     }
    response = requests.request("PATCH",url_f, headers=headers, data=payload)
    return response

def ngsi_get_current(entity, url= "localhost:1026",entity_type='Stress'):
    """
    The function gets the value on an NGSI entity using get request  to orion context broker
    """
    url_o = f"http://{url}/v2/entities/{entity}"
  #  "http://192.168.32.144:1026/v2/entities/urn:ngsi-ld:Stress:001?options=keyValues&type=Stress"
  #  url = f'http://localhost:1026/v2/entities/' + entity +'/attrs?type=Stress'
    headers = {
  #      'Content-Type':"application/json"
  #      'fiware-service': 'openiot',
  #      'fiware-servicepath': '/'
     }
    payload ={}
    response = requests.request("GET", url_o, headers=headers, data=payload)
    return response.json()


