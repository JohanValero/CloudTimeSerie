from flask import Flask
from sqlalchemy import create_engine
from google.cloud import storage
from sklearn.ensemble import IsolationForest

import pandas as pd
import os
import pickle

cMODEL_FILE_NAME = 'my_model.pck'
app = Flask(__name__)

# ################################################################################
# Crea la conexión con la base de datos.
# ################################################################################
vConnection = ("mysql+mysqlconnector://{username}:{password}@{host}:{port}/{schema}").format(
    username = os.getenv('DATABASE_USERNAME'),
    password = os.getenv('DATABASE_PASSWORD'),
    host     = os.getenv('DATABASE_HOST'),
    port     = os.getenv('DATABASE_PORT'),
    schema   = os.getenv('DATABASE_SCHEMA')
)
vConnection = create_engine(vConnection)

# ################################################################################
# Microservicio prinicipal, se encarga de extraer los datos en la base de
# datos, descargar el modelo predictivo, y predecir las anomalias del 
# modelo predictivo.
#
# Author: Johan Pool Valero Perez
# ################################################################################
@app.route('/')
def main_app():
    # Obtiene los datos de la base de datos.
    vDataFrame = pd.read_sql('SELECT * FROM taxi_rides_0002', con = vConnection)
    
    # Descarga el modelo predictivo.
    vStorageClient = storage.Client()
    vBucket = vStorageClient.bucket(os.getenv('BUCKET_NAME'))
    vBlob = vBucket.blob(os.getenv('BLOB_MODEL_FILE'))
    vBlob.download_to_filename(cMODEL_FILE_NAME)

    # Carga el modelo predictivo descargado.
    vModel = None
    with open(cMODEL_FILE_NAME, 'rb') as vFile:
        vModel = pickle.load(vFile)
    
    # Predicce las anomalias en la serie de tiempo.
    vDataFrame['outliers'] = pd.Series(
            vModel.predict(vDataFrame[['value']])
        ).apply(lambda x: 'yes' if (x == -1) else 'no')
    vDataAnomalias = vDataFrame.query('outliers=="yes"')
    
    # Genera el JSON de salida con los resultados.
    vJSON = '{"serie_total": ' + \
                str(vDataFrame.to_json(orient = 'records', lines = False)) + \
            ', "serie_anomalias": ' + \
                str(vDataAnomalias.to_json(orient = 'records', lines = False)) + \
            '}'
    return vJSON

# ################################################################################
# Entrena el modelo el modelo predictivo y lo guarda en "Cloud Storage" para su
# posterior uso por el método [main_app].
#
# Author: Johan Pool Valero Perez
# ################################################################################
@app.route('/train_model')
def train_model():
    # Extrae la serie de tiempo de la base de datos.
    vDataFrame = pd.read_sql('SELECT * FROM taxi_rides_0002', con = vConnection)
    
    # Crea el modelo predictivo y lo entrena. 
    vModel = IsolationForest(contamination = 0.004)
    vModel.fit(vDataFrame[['value']])
    
    # Guarda el modelo predictivo en un archivo.
    with open(cMODEL_FILE_NAME, 'wb') as vFile:
        pickle.dump(vModel, vFile)
    
    # Genera conexión con "Cloud Storage".
    vStorageClient = storage.Client()
    vBucket = vStorageClient.bucket(os.getenv('BUCKET_NAME'))
    vBlob = vBucket.blob(os.getenv('BLOB_MODEL_FILE'))
    
    # Sube el archivo del modelo predictivo como una nueva versión.
    vBlob.upload_from_filename(cMODEL_FILE_NAME)

    return '{"STATUS": 200, "MESSAGE": "OK"}'

gPORT = os.getenv('PORT', default=None)
gAUTHOR_NAME = os.getenv("AUTHOR", default=None)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = gPORT)