import logging
from model import connect_to_db, db, Language, Volunteer

TWILIO_NUMBER = "+16787374363"

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
