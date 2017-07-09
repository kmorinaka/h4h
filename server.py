import os
import sys
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from twilio.twiml.messaging_response import MessagingResponse

from model import connect_to_db, db, Language, Volunteer

app = Flask(__name__)

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


@app.route('/new', methods=['GET'])
def new():
    """ Display new volunteer form with all languages """
    languages = Language.query.all()

    return render_template("new.html", languages=languages)


@app.route('/volunteer/', methods=['POST'])
def create():
    """" Create a new volunteer record from incoming form data """

    fname = request.form.get('first')
    lname = request.form.get('last')
    phone = request.form.get('phone')

    new_volunteer = Volunteer(first_name=fname, last_name=l_name, phone=phone, active=True)
    db.session.add(new_volunteer)
    db.session.commit()

    return redirect("/volunteer/%s" % new_volunteer.volunteer_id)


@app.route('/volunteer/<id>', methods=['GET'])
def show(id):
    """ Show profile of volunteer """

    volunteer = Volunteer.query.get(id)

    return render_template("profile.html", volunteer=volunteer)


@app.route('/volunteer/<id>/edit', methods=['GET'])
def edit(id):
    """" Show a prefilled volunteer form for editing """
    volunteer = Volunteer.query.get(id)

    return render_template("edit.html")


@app.route('/volunteer/<id>', methods=['PUT'])
def update(id):
    """ Update volunteer record """

    fname = request.form.get('first')
    lname = request.form.get('last')
    phone = request.form.get('phone')
    active = request.form.get('active')

    volunteer = Volunteer.query.get(id)
    if fname != volunteer.first_name:
        volunteer.first_name = fname
    if lname != volunteer.lname:
        volunteer.last_name = lname
    if phone != volunteer.phone:
        volunteer.phone = phone
    if active != volunteer.active:
        volunteer.active = active

    db.session.commit()

    return redirect("/volunteer/%s" % id)


if __name__ == "__main__":
  app.debug = True
  connect_to_db(app)
  DebugToolbarExtension(app)
  app.run(host="0.0.0.0")
