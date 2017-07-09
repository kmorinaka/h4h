import os
import sys
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from utils import *
from model import connect_to_db, db, Language, Volunteer, VolunteerLanguage

app = Flask(__name__)

app.secret_key = "ABC"
# Your Account SID from twilio.com/console
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
# Your Auth Token from twilio.com/console
auth_token  = os.environ.get("TWILIO_ACCOUNT_AUTH_TOKEN")
client = Client(account_sid, auth_token)

@app.route('/sms', methods=['GET', 'POST'])
def sms_handle():
    """Handles incoming text messages by sending notification to volunteers"""
    if is_volunteer(request.form['From']):
        event_occurred = grab_event(request.form['Body'])
        if event_occurred and event_occurred.confirmed == False:
            client.messages.create(
            to=request.form['From'],
            from_=TWILIO_NUMBER,
            body=format_send_user_message(event_occurred.message))
            confirm_event(event_occurred.event_id)
    else:
        event_id = create_event(request.form['From'], request.form['Body'])
        numbers, language = get_volunteer_numbers(request.form['Body'])
        for num in numbers:
            client.messages.create(
            to=phone_number_formatter(num),
            from_=TWILIO_NUMBER,
            body=format_acceptance_message(event_id, language))
    return ""

@app.route('/sms', methods=['POST'])
def sms_reply():
    pass

@app.route('/')
def index():

    all_langs = []
    for v_l in VolunteerLanguage.query.all():
        all_langs.append(Language.query.filter_by(language_id=v_l.l_id).one())
    print all_langs
    return render_template("homepage.html", languages=all_langs)


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


    return redirect("/volunteers/all")


@app.route('/volunteer/<id>/edit', methods=['GET'])
def edit(id):
    """" Show a prefilled volunteer form for editing """
    languages = Language.query.all()
    volunteer = Volunteer.query.get(id)

    return render_template("edit.html", volunteer=volunteer,languages=languages)

@app.route('/volunteers/all', methods=['GET'])
def volunteers():

  volunteers = Volunteer.query.all().order_by(last_name)

  return render_template("volunteers.html", volunteers=volunteers)


@app.route('/volunteer/<id>', methods=['POST'])
def update(id):
    """ Update volunteer record """

    fname = request.form.get('first')
    lname = request.form.get('last')
    phone = request.form.get('phone')
    photo = request.form.get('photo')
    active = request.form.get('active')
    print active

    volunteer = Volunteer.query.get(id)
    if fname != volunteer.first_name:
        volunteer.first_name = fname
    if lname != volunteer.last_name:
        volunteer.last_name = lname
    if phone != volunteer.phone:
        volunteer.phone = phone
    if active != volunteer.active:
        volunteer.active = active
    if photo != volunteer.photo:
        volunteer.photo = photo

    # Determine changes in language set for volunteer
    new_languages = set(request.form.getlist('languages'))
    old_languages = {lang.language for lang in volunteer.languages}
    languages_to_add = new_languages - (new_languages & old_languages)
    languages_to_remove = old_languages - new_languages

    # Update languages
    for language in languages_to_add:
        language_id = Language.get_id_by_language(language)
        db.session.add(VolunteerLanguage(v_id=id, l_id=language_id))
    for language in languages_to_remove:
        language = Language.query.filter_by(language=language).one()
        db.session.delete(language)

    db.session.commit()
    return redirect("/volunteers/all")


if __name__ == "__main__":
  app.debug = False

  connect_to_db(app)

  # Use the DebugToolbar
  DebugToolbarExtension(app)

  app.run(host="0.0.0.0")
