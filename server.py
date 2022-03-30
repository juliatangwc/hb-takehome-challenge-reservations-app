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

@app.route("/users", methods=["POST"])
def create_account():
    """Create an account for new users."""
    
    email = request.form.get("email")
    password = request.form.get("password")

    user_exist = helper.get_user_by_email(email)

    if user_exist:
        flash ("This email is already registered on our website. Please log in.")
    else:
        user = helper.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash ("Account created.")

        user_id = user.user_id
        session['user_id'] = user_id
    
    return redirect (f"/user/{user_id}")

@app.route("/login", methods=["POST"])
def log_in():
    """Existing user log in."""

    email = request.form.get("email")
    password = request.form.get("password")
    
    user_exist = helper.get_user_by_email(email)

    if user_exist:
        checked_user = helper.check_user_password(email, password)
        if checked_user:
            user_id = checked_user.user_id
            session['user_id'] = user_id
            flash ("Success! You are logged in!")
            return redirect (f"/user/{user_id}")
        else:
            flash ("Wrong password. Please try again.")
            return redireect("/")
    else:
        flash ("No match for email entered. Please create an account.")
        return redirect("/")

@app.route("/user/<user_id>")
def show_reservations_by_user(user_id):
    """Show all reservations made by a user."""

    reservations = helper.show_all_reservation(user_id)

    return render_template("user.html", reservations = reservations)

@app.route("/reservation-form")
def show_reservation_form():
    """Show reservation form"""
    return render_template("reservation-form.html")

@app.route("/available")
def show_available_slots():
    """Show all available slots according to criteria given."""
    return render_template("available-timeslots.html")

@app.route("/reserve", methods=["POST"])
def make_reservation():
    """Make reservation. Assign a user to a slot."""
    pass



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
