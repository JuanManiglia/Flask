from flask import Flask, flash,  request, render_template, redirect, url_for
import os
import git
import pickle
import pandas as pd

app = Flask(__name__)
app.config['DEBUG'] = True

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv','txt'}

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
def home():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/predict", methods=['POST'])
def predict():
    
    if 'predictionfile' not in request.files:
        flash('No file part')
        return redirect(url_for(home))
    file = request.files['predictionfile']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for(home))
    if file and allowed_file(file.filename):
        #filename = secure_filename(file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        datos = pd.read_csv(file)
        tamano = len(datos)
        model = pickle.load(open('/home/jmaniglia/Flask/ad_model.pkl', 'rb'))
        prediction = model.predict(datos)
        
        if tamano>1:
            tabla = pd.DataFrame(datos,columns=datos.columns)
            tabla['prediction'] = prediction
            resultado = ['safe' if p==1 else 'not safe' for p in prediction ]
            #tabla_html=tabla.to_html()
            return render_template('predict_table.html',tabla=resultado)
        elif tamano==1:
            return render_template('predict.html',resultado=prediction[0])



if __name__ == '__main__':
    app.run()