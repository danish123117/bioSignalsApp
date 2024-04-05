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

def ngsi_get_historical(entity, window_length=5000, url="localhost:8080" , attribute = "data"): 
    """
    The function queries historical data from TimescaleDB using mintaka API 
    """
    url = f"http://{url}/temporal/entities/{entity}"
    payload ={}
    headers = {
        'NGSILD-Tenant': 'openiot',
        'Link': '"<http://context/ngsi-context.jsonld>"; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    params = {
        'lastN': window_length,
        'attrs': attribute
        }
    response = requests.request("GET",url, headers=headers, params=params,data= payload)
   # if response.status_code == 200:
    return response.json()

def ngsi_patch(data,entity,url ="localhost:1026"):
    """
    The function update the value on an NGSI entity using patch to orion context broker
    """
    url = f"http://{url}/ngsi-ld/v1/entities/{entity}/attrs"
    headers = {
        'Content-Type':"application/json",
        "Link": '"<http://context/ngsi-context.jsonld>"; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
     }
    response = requests.patch(url, headers=headers, json=data)
    return response