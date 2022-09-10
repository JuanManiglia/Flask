from flask import Flask
import os
import git


os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/',methods=['GET'])
def hello():
    return "Mi primera API Flask CUTRE"



if __name__ == '__main__':
    app.run()