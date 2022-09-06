from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def main_app():
    return ""

@app.route('/hello_world')
def hello():
    vStringData = "Hola mundo de " + str(gAUTHOR_NAME) + " in port [" + str(gPORT) + "]."
    return vStringData


gPORT = os.getenv('PORT', default=None)
gAUTHOR_NAME = os.getenv("AUTHOR", default=None)

print("PORT: ", gPORT)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = gPORT)