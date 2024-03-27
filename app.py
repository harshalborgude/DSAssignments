import pickle
from flask import Flask,request,jsonify,render_template
# Add this below libraries in requirement.txt file as we have to install them, and run cmd on terminal "pip install -r requirements.txt"
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

## Run cmd : python app.py
## import ridge regressor model and standard scaler pickle

standard_scaler = pickle.load(open("models/9.scaler.pkl","rb"))
ridge_model = pickle.load(open("models/9.ridge.pkl","rb"))

## Rout for home page
## App URL for this app : https://green-translator-qwfjs.pwskills.app:5000/
@app.route("/")
def index():
    return render_template("index.html")

# URL : https://green-translator-qwfjs.pwskills.app:5000/predictdata
# For GET request it will return html file
@app.route("/predictdata",methods=["POST","GET"])
def predict_datapoint():
    if request.method == 'POST':
        Temperature = float(request.form.get('Temperature'))
        RH = float(request.form.get('RH'))
        WS = float(request.form.get('WS'))
        Rain = float(request.form.get('Rain'))
        FFMC = float(request.form.get('FFMC'))
        DMC = float(request.form.get('DMC'))
        ISI = float(request.form.get('ISI'))
        Classes = float(request.form.get('Classes'))
        Region = float(request.form.get('Region'))

        ## Passing new parameters to transform to scaler model in 2D array format
        new_data_scaled = standard_scaler.transform([[Temperature,RH,WS,Rain,FFMC,DMC,ISI,Classes,Region]])
        result = ridge_model.predict(new_data_scaled)
        return render_template('home.html',result=result[0])
    else :
        return  render_template("home.html")

if __name__=="__main__":
    app.run(host="0.0.0.0")
