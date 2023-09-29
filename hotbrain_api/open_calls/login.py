from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from tools.db_con import get_db_instance

from tools.logging import logger

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user

    if not request.form['username'] and not request.form['password']:
        return json_response(status_ = 400, message = "Bad request", authenticated = False)

    db,cur = get_db_instance()

    cur.execute("SELECT * FROM Users WHERE Username = %s", (request.form['username'],))
    if cur.rowcount != 1:
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )

    user = cur.fetchone();

    # TODO: Password Authentication

    jwt = {
            "sub" : request.form['username'] #sub is used by pyJwt as the owner of the token
            }

    return json_response( token = create_token(jwt) , authenticated = True)

