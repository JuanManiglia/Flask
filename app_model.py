from flask import Flask, jsonify, request, render_template
from flask.wrappers import Response
import os
import pandas as pd
import numpy as np
import pickle
import git
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error

app = Flask(__name__)


@app.route('/',methods=['GET'])
def index():
    print(os.getcwd())
    return render_template("index.html")

@app.route('/api/v1/predict', methods=['GET'])
def predict():

    model = pickle.load(open('ad_model.pkl','rb'))
    tv = int(request.args.get('tv',None))
    radio = int(request.args.get('radio',None))
    newspaper = int(request.args.get('newspaper',None))


    if tv is None or radio is None or newspaper is None:
        return "Error no puede ser vacio"
    else:
        prediction = model.predict([[tv,radio,newspaper]])
 

    return jsonify({'prediction':prediction[0]})

@app.route('/api/v1/retrain', methods=['PUT'])
def retrain():
    data = pd.read_csv('data/Advertising.csv', index_col=0)

    ###limpieza.....

    X_train, X_test, y_train, y_test = train_test_split(data.drop(columns=['sales']),
                                                    data['sales'],
                                                    test_size = 0.20,
                                                    random_state=42)

    model = Lasso(alpha=6000)
    model.fit(X_train, y_train)

    pickle.dump(model, open('ad_model.pkl', 'wb'))

    return "Model retrained. New evaluation metric RMSE: " + str(np.sqrt(mean_squared_error(y_test, model.predict(X_test))))




if __name__ == '__main__':
    app.run()