import logging
import os
import detectlanguage
from model import connect_to_db, db, Language, Volunteer

TWILIO_NUMBER = "+16787374363"
detectlanguage.configuration.api_key = os.environ.get("DETECTLANGUAGE_API_KEY")

def get_volunteer_numbers():
    volunteers = Volunteer.query.all()
    return [v.phone for v in volunteers]


def format_recieved_message(user_number, message):
    # TODO: update message without user_number
    return """Hi Polyglot! Someone needs your translation assistance at {}.
              Here's their message: {}""".format(user_number, message)

def format_user_number_message(user_number):
    pass


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
    try:
        Volunteer.query.filter_by(phone=phone_number).one()
        return true
    except NoResultFound:
        return false
    except MultipleResultsFound:
        logging.error("multiple volunteers with number {}".format(phone_number))
        return true
