from flask import Flask
import os

app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello():
    return "Mi primera API Flask CUTRE act desde github hola"



if __name__ == '__main__':
    app.run()