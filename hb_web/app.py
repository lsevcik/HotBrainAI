from flask import Flask, redirect, render_template, session, url_for

from routes.api import api
from database import db_session

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# Import contents of config.cfg to app.config
app.config.from_pyfile("config.cfg")

# Set loglevel to debug
app.logger.setLevel(10)  # DEBUG


@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/login.html")
def login():
    if session.get("logged_in", False):
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/survey.html")
def survey():
    return render_template("survey.html")


@app.route("/matches.html")
def matches():
    return render_template("matches.html")


app.register_blueprint(api, url_prefix="/api")


@app.teardown_appcontext
# pylint: disable=unused-argument
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    import os

    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "8080"))
    except ValueError:
        PORT = 8080
    app.run(HOST, PORT)