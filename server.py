import os
import sys
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from utils import (get_volunteer_numbers,
                   format_recieved_message,
                   phone_number_formatter,
                   is_volunteer,
                   TWILIO_NUMBER)
from model import connect_to_db, db, Language, Volunteer, VolunteerLanguage

app = Flask(__name__)

app.secret_key = "ABC"
# Your Account SID from twilio.com/console
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
# Your Auth Token from twilio.com/console
auth_token  = os.environ.get("TWILIO_ACCOUNT_AUTH_TOKEN")

@app.route('/sms', methods=['GET', 'POST'])
def sms_handle():
    """Handles incoming text messages by sending notification to volunteers"""
    # TODO: should there be a number validator to confirm that the message is not from volunteer?
    # TODO: assign user to volunteer
    # user/volunteer check
    if is_volunteer():
        # TODO: check that event happened
        # TODO: create event
        # TODO: respond to volunteer with user_number
        pass
    else:
        numbers = get_volunteer_numbers()
        client = Client(account_sid, auth_token)
        for num in numbers:
            client.messages.create(
            to=phone_number_formatter(num),
            from_=TWILIO_NUMBER,
            body=format_recieved_message(request.form['From'], request.form['Body']))
    return ""

@app.route('/sms', methods=['POST'])
def sms_reply():
    pass

@app.route('/')
def index():
    return render_template("homepage.html")


@app.route('/new', methods=['GET'])
def new():
    """ Display new volunteer form with all languages """
    languages = Language.query.all()

    return render_template("new.html", languages=languages)


@app.route('/volunteer', methods=['POST'])
def create():
    """" Create a new volunteer record from incoming form data """
    fname = request.form.get('first')
    lname = request.form.get('last')
    phone = request.form.get('phone')
    photo = request.form.get('photo')
    languages = request.form.getlist('languages')
    new_volunteer = Volunteer(first_name=fname, last_name=lname, phone=phone, photo=photo, active=True)
    db.session.add(new_volunteer)
    db.session.commit()

    for language in languages:
        language_id = Language.query.filter_by(language=language).one().language_id
        volunteer_language = VolunteerLanguage(v_id=new_volunteer.volunteer_id, l_id=language_id)
        db.session.add(volunteer_language)
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

    # Determine changes in language set for volunteer
    new_languages = set(request.form.getlist('languages'))
    old_languages = {lang.language for lang in new_languages}
    languages_to_add = new_languages - new_languages & old_languages
    languages_to_remove = old_languages - new_languages

    # Update languages
    for language in languages_to_add:
        language_id = Language.get_id_by_language(language)
        db.session.add(VolunteerLanguage(v_id=id, l_id=language_id))
    for language in languages_to_remove:
        language_id = Language.get_id_by_language(language)
        db.session.delete(VolunteerLanguage(v_id=id, l_id=language_id))

    db.session.commit()
    return redirect("/volunteer/%s" % id)


if __name__ == "__main__":
  app.debug = True

  connect_to_db(app)

  # Use the DebugToolbar
  DebugToolbarExtension(app)

  app.run(host="0.0.0.0")
