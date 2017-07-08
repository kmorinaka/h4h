from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
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
    # create new volunteer with form params
    # then redirect profile page
    # pass id
    id = 1
    return redirect("/volunteer/%s" % id)

@app.route('/volunteer/:id', methods=['GET'])
def show():
    # query with id
    # show volunteer info

    return render_template("profile.html")

@app.route('/volunteer/:id/edit', methods=['GET'])
def edit():
    #  show info in form to be edited

    return render_template("edit.html")

@app.route('/volunteer/:id', methods=['PUT'])
def update():
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
