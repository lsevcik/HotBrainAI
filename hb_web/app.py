from flask import Flask, redirect, render_template, session, url_for, g
from sqlalchemy import select
import qrcode
import qrcode.image.svg

from routes.api import api
from database import db_session

import models

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# Import contents of config.cfg to app.config
app.config.from_pyfile("config.cfg")

# Set loglevel to debug
app.logger.setLevel(10)  # DEBUG


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    if session.get("logged_in", False):
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/survey")
def survey():
    if not session.get("logged_in", False):
        redirect(url_for("login"))
    return render_template("survey.html")


@app.route("/matches")
def matches():
    if not session.get("logged_in", False):
        redirect(url_for("login"))
    stmt = (
        select(models.Match)
        .where(
            models.Match.user1 == session.get("user_userid")
            or models.Match.user2 == session.get("user_userid")
        )
        .limit(10)
    )

    g.matches = db_session.execute(stmt).all()

    app.logger.debug(g.matches)

    return render_template("matches.html")


@app.route("/qr")
def qr():
    if not session.get("logged_in", False):
        redirect(url_for("login"))
    g.img = (
        qrcode.make(
            str(session.get("user_userid", "0")).encode("UTF-8"),
            image_factory=qrcode.image.svg.SvgPathFillImage)
        .to_string()
        .decode("UTF-8")
    )
    return render_template("qr.html")




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