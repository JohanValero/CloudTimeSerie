from flask import Flask
from sqlalchemy import create_engine
from google.cloud import storage
from sklearn.ensemble import IsolationForest

import pandas as pd
import os
import pickle

app = Flask(__name__)

vConnection = ("mysql+mysqlconnector://{username}:{password}@{host}:{port}/{schema}").format(
    username = os.getenv('DATABASE_USERNAME'),
    password = os.getenv('DATABASE_PASSWORD'),
    host     = os.getenv('DATABASE_HOST'),
    port     = os.getenv('DATABASE_PORT'),
    schema   = os.getenv('DATABASE_SCHEMA')
)
vConnection = create_engine(vConnection)

@app.route('/')
def main_app():
    vDataFrame = pd.read_sql('SELECT * FROM taxi_rides_0002', con = vConnection)
    
    vModel =  IsolationForest(contamination = 0.004)
    vModel.fit(vDataFrame[['value']])
    vDataFrame['outliers'] = pd.Series(
            vModel.predict(vDataFrame[['value']])
        ).apply(lambda x: 'yes' if (x == -1) else 'no')
    vDataAnomalias = vDataFrame.query('outliers=="yes"')
    
    vJSON = '{"serie_total": ' + \
                str(vDataFrame.to_json(orient = 'records', lines = False)) + \
            ', "serie_anomalias": ' + \
                str(vDataAnomalias.to_json(orient = 'records', lines = False)) + \
            '}'
    return vJSON

@app.route('/hello_world')
def hello():
    vStringData = "Hola mundo de " + str(gAUTHOR_NAME) + " in port [" + str(gPORT) + "]."
    return vStringData

@app.route('/train_model')
def train_model():
    cMODEL_FILE_NAME = 'my_model.pck'
    vDataFrame = pd.read_sql('SELECT * FROM taxi_rides_0002', con = vConnection)
    vModel = IsolationForest(contamination = 0.004)
    vModel.fit(vDataFrame[['value']])
    
    with open(cMODEL_FILE_NAME, 'wb') as vFile:
        pickle.dump(vModel, vFile)
    
    vStorageClient = storage.client()
    vBucket = vStorageClient.bucket(os.getenv('BUCKET_NAME'))
    vBlob = vBucket.blob(os.getenv('BLOB_MODEL_FILE'))
    vBlob.upload_from_filename(cMODEL_FILE_NAME)

    return '{"STATUS": 200, "MESSAGE": "OK"}'

gPORT = os.getenv('PORT', default=None)
gAUTHOR_NAME = os.getenv("AUTHOR", default=None)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = gPORT)