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
        "zeroCrossingFrequency": {
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
        }
    params = {
        'lastN': window_length
        }
    response = requests.request("GET",url, headers=headers, params=params,data= payload)
   # if response.status_code == 200:
    return response.json()

def ngsi_patch(data,entity,entity_type,url ="localhost:1026"):
    """
    The function update the value on an NGSI entity using patch to orion context broker
    """
    url = f"http://{url}/v2/entities/{entity}/attrs/?type={entity_type}"
  #  url = f'http://localhost:1026/v2/entities/' + entity +'/attrs?type=Stress'
    headers = {
        'Content-Type':"application/json"
  #      'fiware-service': 'openiot',
  #      'fiware-servicepath': '/'
     }
    response = requests.patch(url, headers=headers, json=data)
    return response


