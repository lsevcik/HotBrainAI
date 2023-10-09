from flask import Flask, render_template, request, redirect, url_for, g, config, session
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import sys
import datetime
import bcrypt
import traceback
import yaml
import logging

from tools.db_con import get_db

from tools.token_required import token_required
from tools.session import start_session

app = Flask(__name__)

app.config.from_file("config.yml", load=yaml.safe_load)

app.logger.setLevel(logging.DEBUG)

app.secret_key = b"abc123"

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


@app.route("/user_api/<proc_name>", methods=["GET", "POST"])
@token_required
@start_session
def exec_secure_proc(proc_name):
    try:
        fn = getattr(__import__("user_calls." + proc_name), proc_name)
        return fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + "\n"
        ex_data = ex_data + str(err) + "\n"
        ex_data = ex_data + traceback.format_exc()
        app.logger.error(ex_data)
        return json_response(status_=500, data="Internal Server Error")


@app.route("/open_api/<proc_name>", methods=["GET", "POST"])
def exec_open_proc(proc_name):
    try:
        fn = getattr(__import__("open_calls." + proc_name), proc_name)
        return fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + "\n"
        ex_data = ex_data + str(err) + "\n"
        ex_data = ex_data + traceback.format_exc()
        app.logger.error(ex_data)
        return json_response(status_=500, data="Internal Server Error")


@app.route("/scanner_api/<proc_name>", methods=["GET", "POST"])
@token_required
def exec_scanner_proc(proc_name):
    try:
        fn = getattr(__import__("scanner_calls." + proc_name), proc_name)
        return fn.handle_request()
    except Exception as err:
        ex_data = str(Exception) + "\n"
        ex_data = ex_data + str(err) + "\n"
        ex_data = ex_data + traceback.format_exc()
        app.logger.error(ex_data)
        return json_response(status_=500, data="Internal Server Error")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
