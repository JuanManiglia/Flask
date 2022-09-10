from flask import Flask
import os
import git

app = Flask(__name__)

# Route for the GitHub webhook

@app.route('/git_update', methods=['POST'])
def git_update():
    repo = git.Repo('./Flask')
    origin = repo.remotes.origin
    repo.create_head('main',
                     origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return '', 200

@app.route('/',methods=['GET'])
def hello():
    return "Mi primera API Flask CUTRE act desde github 200"



if __name__ == '__main__':
    app.run()