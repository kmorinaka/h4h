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
    return "Hi Volunteer! Incoming Message from number {}: {}".format(user_number, message)

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
