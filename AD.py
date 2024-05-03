import time
import json
import os
import numpy as np
import ngsiOperations.ngsiv2Operations.ngsiv2CrudOperations as v2
import helperFunctions.helperFunctions as hp
import bioTools.emgTools as emg


def anomaly_detector(entity_sensor,entity_stress):
    '''The looped part has an execution time of ~0.065 seconds'''
    entity = entity_sensor# entity_sensor#  holds emg data eg. 'urn:ngsi-ld:Operator:001'
    entity2 =  entity_stress# holds stress state as mean, median and mean power frequencies e.g. 'urn:ngsi-ld:Stress:001'
    window_length = 200
    script_dir = os.path.dirname(os.path.abspath(__file__))
    params_path = os.path.join(script_dir, 'parms.json')
    with open(params_path, 'r') as json_file:
        parms = json.load(json_file)
      
    time.sleep(5)
    while True:
        start_time = time.time()
        data = v2.ngsi_get_historical('Thing:EMG1000',window_length)
        #if data ==0:     # case when the there is no data transmission
            # do something when error code is returned probably skip the code   
        
        data_arr= hp.data_to_np(data) # convert data from timescaleDB to np array shape (6, window length) this is transposed
        filter_data = emg.data_filter(data_arr,sampling_frequency=1000,band_lower=20,band_upper=450) # applies band pass filter shape is still (6,window lenght) check if it works
        median_frequency , mean_frequency, mean_power_frequency, zero_cross_frequency = emg.out_stft(np.transpose(filter_data),sampling_frequency=1000) # extracted features , these should be 3 (1x8) lists 
        #print(median_frequency)
        #print(mean_frequency)
        #print(mean_power_frequency)
        #print(zero_cross_frequency)
        s_mean, s_med, s_mpower, s_zcf = emg.stress_out(mean_frequency, median_frequency, mean_power_frequency,zero_cross_frequency, parms) # stress level 
        #print(s_mean, s_med, s_mpower, s_zcf)
        payload_raw = v2.stress_payload(s_mean.tolist(), s_med.tolist(), s_mpower.tolist(), s_zcf.tolist() )    
        json_data = json.dumps(payload_raw)
        #print(payload_raw)
        resp = v2.ngsi_patch(json_data,entity2)
        print(resp.status_code)
        #print(time.time() - start_time)
        if (time.time() - start_time) < 5:
            time.sleep(5- (time.time() - start_time))

if __name__ =="__main__":
    print("Welcome to UC1_AD")
