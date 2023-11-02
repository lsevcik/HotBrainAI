from modulefinder import AddPackagePath
from flask import Flask, redirect, render_template, request, session, url_for, g
from sqlalchemy import select
import qrcode
import qrcode.image.svg
from models.user import User, Gender, GenderClass, Seeking, UserSeeking

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


@app.route("/survey", methods=["GET", "POST"])
def survey():
    if not session.get("logged_in", False):
        redirect(url_for("login"))
        
    stmt = select(User).where(User.id == session.get("user_userid"))
    result = db_session.execute(stmt)
    user = result.scalar_one_or_none()

    if (request.method == "GET"):
        g.user = user
        g.user_seeking = [str(s.seeking) for s in user.seeking]
        return render_template("survey.html")
    
    app.logger.debug(request.form)
    
    user.first_name = request.form["fname"]
    user.last_name = request.form["lname"]
    user.gender = Gender[request.form["gr"]]
    user.gender_class = GenderClass[request.form["gi"]]
    user.only_cisgender = request.form["interest"] == "YES"

    stmt = UserSeeking.__table__.delete().where(UserSeeking.user_id == user.id)
    db_session.execute(stmt)

    db_session.flush()
    for s in request.form.getlist("sex"):
        user.seeking += [UserSeeking(user_id=user.id, seeking=Seeking[s])]
        
    db_session.commit()
    
    return redirect(url_for("survey"))


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