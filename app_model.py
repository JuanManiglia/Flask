from flask import Flask, flash,  request, render_template, redirect, url_for, session
import os
import git
import pickle
import pandas as pd
from sales_form import SalesForm
from random import randint

app = Flask(__name__)
app.config['DEBUG'] = True

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv','txt'}
app.config["SECRET_KEY"] = "12345678"

# Route for the GitHub webhook

@app.route('/git_update', methods=['POST'])
def git_update():
    repo = git.Repo('./Flask')
    origin = repo.remotes.origin
    repo.create_head('main',
                     origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return '', 200

@app.route("/", methods=['GET'])
def index():

    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/predict", methods=['POST'])
def predict():
    
    if 'predictionfile' not in request.files:
        flash('No file part')
        return redirect(url_for(index))
    file = request.files['predictionfile']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for(index))
    if file and allowed_file(file.filename):
        #filename = secure_filename(file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        val = randint(0,200)
        datos = pd.read_csv(file, index_col=0)
        prueba = datos.iloc[val-1:val,:-1]
        tamano = len(prueba)
        model = pickle.load(open('ad_model.pkl', 'rb'))
        prediction = model.predict(prueba)
        
        # if tamano>1:
        #     tabla = pd.DataFrame(datos,columns=datos.columns)
        #     tabla['prediction'] = prediction
        #     resultado = ['safe' if p==1 else 'not safe' for p in prediction ]
        #     #tabla_html=tabla.to_html()
        #     return render_template('predict_table.html',tabla=tabla.to_html())
        if tamano==1:
            return render_template('predict.html',resultado=int(prediction[0]))
        else:
            return 'ERROr 404'



if __name__ == '__main__':
    app.run()