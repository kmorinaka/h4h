from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///humanity'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


class Volunteer(db.Model):
    """ Language volunteer info """

    __tablename__ = "volunteers"

    volunteer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(10))
    active = db.Column(db.Boolean())


class Language(db.Model):
    """ Table of all languages """

    __tablename__ = "languages"

    language_id = Column(db.Integer, autoincrement=True, primary_key=True)
    language = db.Column(db.String(15), unique=True)


class VolunteerLanguage(db.Model):
    """ Association Table for volunteers and languages """

    __tablename__ = "volunteerlanguage"

    vl_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    v_id = db.Column(db.Integer, db.Integer, db.ForeignKey('volunteers.volunteer_id'))
    l_id = db.Column(db.Integer, db.Integer, db.ForeignKey('languagess.language_id'))


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
