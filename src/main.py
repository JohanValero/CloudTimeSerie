from venv import create
from flask import Flask
from sqlalchemy import create_engine

import pandas as pd
import os

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
    vJSON = vDataFrame.to_json(orient = 'records', lines = True)
    return vJSON

@app.route('/hello_world')
def hello():
    vStringData = "Hola mundo de " + str(gAUTHOR_NAME) + " in port [" + str(gPORT) + "]."
    return vStringData

gPORT = os.getenv('PORT', default=None)
gAUTHOR_NAME = os.getenv("AUTHOR", default=None)

print("PORT: ", gPORT)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = gPORT)