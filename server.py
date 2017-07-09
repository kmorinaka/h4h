import os
import sys
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from twilio.twiml.messaging_response import MessagingResponse

from model import connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
# Your Account SID from twilio.com/console
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
# Your Auth Token from twilio.com/console
auth_token  = os.environ.get("TWILIO_ACCOUNT_AUTH_TOKEN")

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

@app.route('/sms', methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming text messages"""
    # The sender's phone number is available in payload
    number = request.form['From']
    message_body = request.form['Body']

    resp = MessagingResponse()
    # generic message for now
    resp.message('Hello {}, you said: {}'.format(number, message_body))
    return str(resp)

@app.route('/')
def index():
    return render_template("homepage.html")



if __name__ == "__main__":
  # We have to set debug=True here, since it has to be True at the point
  # that we invoke the DebugToolbarExtension
  app.debug = True

  connect_to_db(app)

  # Use the DebugToolbar
  DebugToolbarExtension(app)

  app.run(host="0.0.0.0")
