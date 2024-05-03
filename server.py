from flask import Flask , render_template, request
from ngsiOperations.ngsiv2Operations.ngsiv2EntityCreator import ngsi_create_trial
from ngsiOperations.ngsiv2Operations.ngsiv2SensorProvision import sensor_provision
from ngsiOperations.ngsiv2Operations.ngsiv2Subscriptions import createSubscriptions
from AD import*
from CEP import*
from waitress import serve
import threading
import queue
#client = None
#client_queue = queue.Queue()
app = Flask(__name__)

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/setup')

def create_Trial():
    # could add health check as a route to render failure message
    trial_name = request.args.get("trial name")
    # Add exception handler.
   # if not bool(trial_name.strip()):
        # add details message that trial name cannot be empty
     #   return render_template("trial_fail.html")
    global stress_entity
    global sensor_entity
    #stress_entity= "urn:ngsi-ld:Stress_" +trial_name +":001"
    #sensor_entity = "urn:ngsi-ld:Sensor_" +trial_name+":001"
    stress_entity= "Stress:005" 
    sensor_entity = "Sensor:005" 
      # this could create potential issues in subscriptions
    resp_stress , resp_sensor = ngsi_create_trial(sensor = sensor_entity,stress=stress_entity)
    #if resp_stress.status_code !=200 or resp_sensor.status_code != 200: 
        #add parameters for response code and messsage related to failure mode 
        # add success message from trial name : Correct
       # return render_template('trial_fail.html')
    
    servicepath_provision_response , sensor_provision_response = sensor_provision(sensor_entity)
    #if servicepath_provision_response.status_code !=200 or sensor_provision_response.status_code != 200: 
        # thete could be other return codes probably better to return something else instead which 
        # circumvents the issue of response codes where the entity/subscription already exists 
        # case for sensor provision 
        #return render_template('trial_fail.html')
    
    subscription_sensor_response, subscription_stress_response = createSubscriptions(trial_name) 
    #if subscription_sensor_response.status_code !=200 or subscription_stress_response.status_code != 200: 
        # some parameters for the response codes
        #return render_template('trial_fail.html')
    
    return render_template(
        '2_run_AD.html',
        trial = trial_name,
        entity_sensor_code= resp_sensor.status_code,
        entity_sensor_message=resp_sensor.text,
        entity_stress_code=resp_stress.status_code,
        entity_stress_message=resp_stress.text,
        prov_servicepath_status=servicepath_provision_response.status_code ,
        prov_servicepath_message=servicepath_provision_response.text ,
        prov_sensor_status=sensor_provision_response.status_code,
        prov_sensor_message =sensor_provision_response.text,
        subs_sensor_code =subscription_sensor_response.status_code, 
        subs_sensor_message=subscription_sensor_response.text,
        subs_stress_code=subscription_stress_response.status_code,
        subs_stress_message =subscription_stress_response.text               
                           )
@app.route('/runAD')
def run_AD():
    #anomaly_detector(sensor_entity,stress_entity)
    client_thread_1 = threading.Thread(target=anomaly_detector_thread, args=(sensor_entity, stress_entity))
    client_thread_1.start()
# how to do this becauee client wont be returned unless you stop the trial
    return render_template('test.html' )
def anomaly_detector_thread(sensor_entity,stress_entity):
    anomaly_detector(sensor_entity,stress_entity)

@app.route('/runCEP')
def run_CEP():
    client_thread_2 = threading.Thread(target=CEP_UC1_thread, args=(stress_entity,))
    client_thread_2.start()
    return render_template('3_stop_trial.html' )
def CEP_UC1_thread(entityStress):
    CEP_UC1(entityStress)

@app.route('/stop')
def stop():
    #stop_trial(client)
    return render_template('index.html')
# something to get data from previus trials this button should be availible on Index 

@app.route('/historypage')
def go_to_history():
    print("this gives me a list of historical")

@app.route('/download')
def download_trial_data():
    print('this downloads the data of a trial')


if __name__ == "__main__":
    serve(app, host= "0.0.0.0", port= 3002)
