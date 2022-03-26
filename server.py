"""Server for reservations app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import helper

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def show_homepage():
    """Show homepage"""
    return render_template("homepage.html")

@app.route("/login", methods=["POST"])
def log_in():
    """Existing user log in."""

    email = request.form.get("email")
    password = request.form.get("password")
    
    user_exist = crud.get_user_by_email(email)

    if user_exist:
        checked_user = crud.check_user_password(email, password)
        if checked_user:
            session['pkey'] = checked_user
            flash ("Success! You are logged in!")
        else:
            flash ("Wrong password. Please try again.")
    else:
        flash ("No match for email entered. Please create an account.")
    
    return redirect ("/reservation-form")

@app.route("/reservation-form")
def show_reservation_form():
    """Show reservation form"""
    return render_template("reservation-form.html")

@app.route("/available")
def show_available slots():
    """Show all available slots according to criteria given."""
    return render_template("available-timeslots.html")

@app.route("/reserve", methods=["POST"])
def make_reservation():
    """Make reservation. Assign a user to a slot."""
    pass

@app.route("/user/<user_id>")
def show_reservations_by_user():
    """Show all reservations made by a user."""

    reservations = helper.all_reservation_list()

    return render_template("user.html", reservations = reservations)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
