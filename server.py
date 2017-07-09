from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db


app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/new', methods=['GET'])
def new():
    """ Display new volunteer form with all languages """
    languages = Language.query.all()

    return render_template("new.html", languages)


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

    return render_template("profile.html", volunteer)


@app.route('/volunteer/<id>/edit', methods=['GET'])
def edit(id):

    volunteer = Volunteer.query.get(id)

    return render_template("edit.html")


@app.route('/volunteer/<id>', methods=['PUT'])
def update(id):

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

  # Use the DebugToolbar
  DebugToolbarExtension(app)

  app.run(host="0.0.0.0")
