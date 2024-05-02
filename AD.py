import time
import json
import os
import numpy as np
import ngsiOperations.ngsiv2Operations.ngsiv2CrudOperations as v2
import helperFunctions.helperFunctions as hp
import bioTools.emgTools as emg


def anomaly_detector(entity_sensor,entity_stress):
    entity = 'Thing:EMG1000'# entity_sensor#  holds emg data eg. 'urn:ngsi-ld:Operator:001'
    entity2 =  entity_stress# holds stress state as mean, median and mean power frequencies e.g. 'urn:ngsi-ld:Stress:001'
    window_length = 5000
    script_dir = os.path.dirname(os.path.abspath(__file__))
    params_path = os.path.join(script_dir, 'parms.json')
    with open(params_path, 'r') as json_file:
        parms = json.load(json_file)
      
    time.sleep(5)
    while True:
        start_time = time.time()
        data = v2.ngsi_get_historical(entity,window_length)
        #if data ==0:     # case when the there is no data transmission
            # do something when error code is returned probably skip the code   
        
        data_arr= hp.data_to_np(data) # convert data from timescaleDB to np array shape (6, window length) this is transposed
        filter_data = emg.data_filter(data_arr) # applies band pass filter shape is still (6,window lenght) check if it works
        median_frequency , mean_frequency, mean_power_frequency, zero_cross_frequency = emg.out_stft(np.transpose(filter_data)) # extracted features , these should be 3 (1x8) lists 
        
        s_mean, s_med, s_mpower, s_zcf = emg.stress_out(mean_frequency, median_frequency, mean_power_frequency,zero_cross_frequency, parms) # stress level 
        
        payload_raw = v2.stress_payload(s_mean, s_med, s_mpower, s_zcf )    
        #json_data = json.dumps(payload_raw)
        v2.ngsi_patch(payload_raw,entity2)
        if (time.time() - start_time) < 5:
            time.sleep(5- time.time() + start_time)

if __name__ =="__main__":
    print("welcome to Ad code")
