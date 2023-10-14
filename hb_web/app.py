from flask import Flask, render_template

from routes.api import api


app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# Import contents of config.cfg to app.config
app.config.from_pyfile("config.cfg")

# Set loglevel to debug
app.logger.setLevel(10) # DEBUG

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/survey")
def survey():
    return render_template("survey.html")

@app.route("/matches")
def matches():
    return render_template("matches.html")

app.register_blueprint(api, url_prefix="/api")

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '8080'))
    except ValueError:
        PORT = 8080
    app.run(HOST, PORT)