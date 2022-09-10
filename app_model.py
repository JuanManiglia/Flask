from flask import Flask
import os

@app.route('/',methods=['GET'])
def hello():
    return "Mi primera API Flask CUTRE act desde github 200"



if __name__ == '__main__':
    app.run()