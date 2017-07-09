import logging
import os
import detectlanguage
from model import connect_to_db, db, Language, Volunteer
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from model import connect_to_db, db, Language, Volunteer, Event

TWILIO_NUMBER = "+16787374363"
detectlanguage.configuration.api_key = os.environ.get("DETECTLANGUAGE_API_KEY")

def get_volunteer_numbers(message):
    language = detect_language(message)
    return phone_numbers_by_language(language)

def format_acceptance_message(event_id):
    return """Hi Polyglot! Someone needs your translation assistance. \nRespond back with the number {} to accept.""".format(event_id)

def grab_event(event_id):
    return Event.query.filter_by(event_id=event_id).scalar()

def confirm_event(event_id):
    event = Event.query.filter_by(event_id=event_id).scalar()
    event.confirmed = True
    db.session.add(event)
    db.session.commit()

def format_send_user_message(message):
    return "Thanks for accepting!  Here's message and phone number at which to followup: {}".format(message)


def phone_number_formatter(phone_number):
    """check that phone number is correct length"""
    if len(phone_number) == 11:
        return "+{}".format(phone_number)
    if len(phone_number) == 10:
        return "+1{}".format(phone_number)
    logging.error("invalid phone number in database: {}".format(phone_number))

def detect_language(text):
    """detects the language a text string is in and returns the language as a string"""
    langs = {
      "en": "English",
      "sp": "Spanish",
      "fr": "French"
    }

    lang_code = detectlanguage.simple_detect(text)

    return langs[lang_code]

def phone_numbers_by_language(language):
    language = Language.query.filter_by(language=language).one()
    return [vol.phone for vol in language.volunteers]


def is_volunteer(phone_number):
    phone_number = phone_number.replace("+1", "")
    try:
        Volunteer.query.filter_by(phone=phone_number).one()
        return True
    except NoResultFound:
        return False
    except MultipleResultsFound:
        logging.error("multiple volunteers with number {}".format(phone_number))
        return True

def create_event(user_number, user_message):
    message = "{}: {}".format(user_number, user_message)
    new_event = Event(message=message, confirmed=False)
    db.session.add(new_event)
    db.session.commit()
    return new_event.event_id
