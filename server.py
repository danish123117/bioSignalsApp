from flask import Flask , render_template, request
from AD import anomaly_detector
from ngsiOperations.ngsiv2Operations.ngsiv2EntityCreator import ngsi_create_trial
from ngsiOperations.ngsiv2Operations.ngsiv2SensorProvision import sensor_provision
from waitress import serve
app = Flask(__name__)

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/runAD')

def create_Trial():
    trial_name = request.get("Trial_name")
    # Add exception handler.
    if not bool(trial_name.strip()):
        # add details message that trial name cannot be empty
        return render_template("trial_fail.html")
    stress_entity= "urn:ngsi-ld:Stress_" +trial_name +":001"
    sensor_entity = "urn:ngsi-ld:" +trial_name+":001"
    resp_stress , resp_sensor = ngsi_create_trial(sensor = sensor_entity,stress=stress_entity)
    if resp_stress.status_code !=200 or resp_sensor.status_code != 200: 
        #add parameters for response code and messsage related to failure mode 
        # add success message from trial name : Correct
        return render_template('trial_fail.html')
    
    servicepath_provision_response , sensor_provision_response = sensor_provision(sensor_entity)
    if servicepath_provision_response.status_code !=200 or sensor_provision_response != 200: 
        #print(sensor_response.status_code)
        #print(sensor_response.text)
        # case for sensor provision 
        return render_template('trial_fail.html')
            


if __name__ == "__main__":
    serve(app, host= "0.0.0.0", port= 3000)
