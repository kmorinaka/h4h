from model import Language, connect_to_db, db
from server import app

connect_to_db(app)

def parse_file():
    file = open('./languages.txt', 'r')
    for line in file:
        lang_name = line.strip('')
        l = Language(language = lang_name)
        db.session.add(l)
    db.session.commit()

parse_file()
