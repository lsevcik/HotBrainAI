from flask import Flask, redirect, render_template, request, session, url_for, g
#from flask_socketio import SocketIO
from sqlalchemy import select
import qrcode
import qrcode.image.svg

from routes.api import api

from models.datapoint import *
from models.match import *
from models.user import *
from database import db_session, init_db

from operator import itemgetter

app = Flask(__name__)
#socketio = SocketIO(app)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# Create config
try:
    app.config.from_pyfile(filename="config.cfg")
except OSError:
    app.logger.warning("Failed to load config.cfg")
app.config.from_prefixed_env()

# Set loglevel to debug
app.logger.setLevel(10)  # DEBUG


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

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
    
    # SQL query to get all matches for current user (Match user_id and score)
    stmt = (
	    select(Match.user1, Match.score)
        .where (
            Match.user2 == session.get("user_userid")
	    ).union (
	        select(Match.user2, Match.score)
            .where (
                Match.user1 == session.get("user_userid")
            )
        )
    )

    g.matches = db_session.execute(stmt).all() # Execute the statement (get all matches)

    user_info = getUserInfo() # Get relevant current user info as a list

    # Parse out matches that do not fit preferences
    for match in g.matches[:]:
        parseMatches(match, user_info)

    sortAndFilterMatches() # Sort the list by lowest score (closest distance) and remove all but top 10

    return render_template("matches.html")

# Get relevant user info as a list for parsing match preferences
def getUserInfo():
    # SQL to get current user
    stmt = select(User).where(User.id == session.get("user_userid"))
    result = db_session.execute(stmt)
    user = result.scalar_one_or_none()

    # Grab only relevant info and place into a list
    only_cis = user.only_cisgender
    user_seeking = user.seeking
    user_gender = str(user.gender).split('.')[1]
    user_gender_class = str(user.gender_class).split('.')[1]
    return [only_cis, user_seeking, user_gender, user_gender_class]

# For each match, remove the ones that do not match both user and match preferences
def parseMatches(match, user_info):
    # SQL to get current match user info
    stmt = select(User).where(User.id == match[0])
    result = db_session.execute(stmt)
    match_user = result.scalar_one_or_none()
    match_gender_class = str(match_user.gender_class).split('.')[1]

    # User ONLY wants Cis and Match is NOT Cis
    if user_info[0] and match_gender_class != "CISGENDER":
        g.matches.remove(match)

    # Match ONLY wants Cis and User is NOT Cis
    elif match_user.only_cisgender and user_info[3] != "CISGENDER":
        g.matches.remove(match)

    # Otherwise both user and match seeking preferences
    else:
        seeks = False

        # For all user preferences, compare to match preferences
        for u_preference in user_info[1]:
            u_seeking = str(u_preference.seeking).split('.')[1]
            match_gender = str(match_user.gender).split('.')[1]
            if u_seeking == match_gender:
                for m_preference in match_user.seeking:
                    m_seeking = str(m_preference.seeking).split('.')[1]
                    if m_seeking == user_info[2]:
                        seeks = True

        # If preferences do not match, remove from list
        if not seeks:
            g.matches.remove(match)

# Sort the matches by best to worst scores (lowest->highest)
# Only display top 10 (remove extra matches)
def sortAndFilterMatches():
    key = 1
    g.matches.sort(key = itemgetter(key)) # Sort by score (ascending)

    # Remove all extra matches from the end of the list (until 10 left)
    for match in reversed(g.matches[:]):
        if len(g.matches) > 10:
            g.matches.remove(match)

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
    init_db()
    app.run(HOST, PORT)