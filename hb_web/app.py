from flask import Flask, render_template
from flask_json import FlaskJSON

import routes.api


app = Flask(__name__)

app.config.from_pyfile("config.cfg")

app.logger.setLevel(10) # DEBUG

FlaskJSON(app)


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

app.register_blueprint(routes.api.api, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
