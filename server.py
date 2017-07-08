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
    # include languages
    return render_template("new.html")


@app.route('/volunteer/', methods=['POST'])
def create():
    """" Create a new volunteer record from incoming form data """

    fname = request.form.get(first)
    lname = request.form.get(last)
    phone = request.form.get(phone)

    new_volunteer = Volunteer(first_name=fname, last_name=l_name, phone=phone, active=True)
    db.session.add(new_volunteer)
    db.session.commit()

    return redirect("/volunteer/%s" % new_volunteer.volunteer_id)


@app.route('/volunteer/<id>', methods=['GET'])
def show(id):
    """ Show profile of volunteer """

    volunteer = Volunteer.query.filter_by(volunteer_id=id)
    languages = VolunteerLanguage.query.filter_by(v_id=id)

    return render_template("profile.html", volunteer)


@app.route('/volunteer/<id>/edit', methods=['GET'])
def edit(id):
    #  show info in form to be edited

    return render_template("edit.html")


@app.route('/volunteer/<id>', methods=['PUT'])
def update(id):
    # update with new params

    id = 1
    return redirect("/volunteer/%s" % id)


if __name__ == "__main__":
  # We have to set debug=True here, since it has to be True at the point
  # that we invoke the DebugToolbarExtension
  app.debug = True

  connect_to_db(app)

  # Use the DebugToolbar
  DebugToolbarExtension(app)

  app.run(host="0.0.0.0")
