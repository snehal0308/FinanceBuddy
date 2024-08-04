import os
from typing import Optional

from dotenv import load_dotenv
from urllib.parse import urlparse
# 📁 server.py -----

import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import send_from_directory


import re

from twilio.twiml.messaging_response import MessagingResponse
import json
from flask import Flask, request, flash
from twilio.twiml.voice_response import VoiceResponse, Start
from twilio.rest import Client
from flask import Flask, request , render_template, request
from twilio.twiml.voice_response import VoiceResponse,Gather
from os import path

from flask import Flask, redirect, render_template, session, url_for, jsonify

from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, find_dotenv
import pprint
from pymongo import MongoClient


import json



from authlib.integrations.flask_client import OAuth

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )
'''
app.config['STATIC_FOLDER'] = 'data'  

@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(app.config['STATIC_FOLDER'], filename)




load_dotenv()
password = os.environ.get("MONGODB_PWD")
connection = f"mongodb+srv://thesnehaladbol:{password}@ex1.sbojxfb.mongodb.net/?retryWrites=true&w=majority&appName=EX1"
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
client = MongoClient(connection)

openai.api_key = ""

initialize db
dbs = client.list_database_names()
videos_db = client.videos
collections = videos_db.list_collection_names()
collection = videos_db.video




@app.route("/")
def home():
    return render_template("index.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route("/dash")
def dashboard():
    return render_template("dash.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
income = "";

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body').lower()

    # Create reply
    resp = MessagingResponse()
    if 'Initialize' in msg:
        resp.message(f"Hi let's set up your accounnt! \n What is your monthly income?")
        mss = msg
    elif "$2000"in msg:
        income = msg
        resp.message(f"Monthly income added as {income}")
        resp.message("Would you like to anything else? \n Here's a list of all commands \n 1)Log an expense: [Expense]  \n 2)Set a reminder to:[Reminder] \n  3) Set a goal to: [Goal]")
    elif "no" in msg :
        resp.message("Thanks for using FinanceBuddy!")
    return str(resp)


@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()

    # Start our <Gather> verb
    gather = Gather(num_digits=1, action='/answer')
    gather.say('to redirect your call, press 1. To end the call, press 2.')
    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/voice')

    return str(resp)




@app.route('/call', methods=['POST'])
def call():
    """Accept a phone call and provide real-time transcription."""
    response = VoiceResponse()
    start = Start()
    start.stream(url=f'wss://{request.host}/stream')
    response.append(start)


    return str(response), 200, {'Content-Type': 'text/xml'}

if __name__ == "__main__":
    app.run(debug=True)





