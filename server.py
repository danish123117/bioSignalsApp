from flask import Flask , render_template, request
from AD import anomaly_detector
from waitress import serve
app = Flask(__name__)

@app.route('/')
@app.route('/index')

def index():
    return "Hello world2"

if __name__ == "__main__":
    serve(app, host= "0.0.0.0", port= 3000)

