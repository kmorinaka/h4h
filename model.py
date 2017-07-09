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
    phone = db.Column(db.String(15))
    photo = db.Column(db.String(300))
    active = db.Column(db.Boolean())

    languages = db.relationship("Language", backref=db.backref("volunteers"), secondary="volunteerlanguage")


class Language(db.Model):
    """ Table of all languages """

    __tablename__ = "languages"

    language_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    language = db.Column(db.String(15), unique=True)

    @classmethod
    def get_id_by_language(cls, language_name):
        return cls.query.filter_by(language = language_name).one().language_id


class VolunteerLanguage(db.Model):
    """ Association Table for volunteers and languages """

    __tablename__ = "volunteerlanguage"

    vl_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    v_id = db.Column(db.Integer, db.ForeignKey('volunteers.volunteer_id'))
    l_id = db.Column(db.Integer, db.ForeignKey('languages.language_id'))


class Event(db.Model):
    """ Each volunteer client match event """

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    message = db.Column(db.Text)
    confirmed = db.Column(db.Boolean())


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
