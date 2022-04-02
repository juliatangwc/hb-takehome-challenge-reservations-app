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
        return redirect("/")
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
    if session['user_id']:
        print('session', session['user_id'], type(session['user_id']))
        if session['user_id'] == int(user_id):
            reservations = helper.show_all_reservation(user_id)
            return render_template("user.html", reservations = reservations)
        else:
            flash("Access not allowed.")
            correct_id = session['user_id']
            return redirect(f"/user/{correct_id}")
    else:
        flash("Please login to view your reservations.")
        return redirect("/")

@app.route("/reservation-form")
def show_reservation_form():
    """Show reservation form"""
    return render_template("reservation-form.html")

@app.route("/available")
def show_available_slots():
    """Show all available slots according to criteria given."""
    
    date = request.args.get("date")
    start = request.args.get("start")
    end = request.args.get("end")

    print(date)
    print(start)
    print(end)

    timeslots = helper.show_available_timeslots(date, start, end)

    return render_template("available-timeslots.html", timeslots = timeslots)

@app.route("/reserve", methods=["POST"])
def make_reservation():
    """Make reservation. Assign a user to a slot."""

    user_id = session["user_id"]
    date = request.form.get("date")
    time = request.form.get("time")

    existing_timeslot = helper.check_user_res_by_date(date, user_id)

    if existing_timeslot:
        flash(f"""You have an existing reservation on {existing_timeslot.date} at {existing_timeslot.time}. 
        Only one reservation is allowed per day.""")
        return redirect("/reservation-form")
    else:
        timeslot = helper.get_timeslot_by_date_time(date, time)
        
        if timeslot.user_id:
            flash("Timeslot taken. Please choose again.")
            return redirect(request.referrer)
        else:
            timeslot.user_id = user_id
            db.session.add(timeslot)
            db.session.commit()   
            flash("Reservation made succesfully.")
            return redirect (f"/user/{user_id}")

@app.route("/edit", methods=["POST"])
def edit_reservation():
    pass

@app.route("/cancel", methods=["POST"])
def delete_reservation():
    user_id = session["user_id"]
    date = request.form.get("date")
    time = request.form.get("time")

    timeslot = helper.get_timeslot_by_date_time(date, time)
    timeslot.user_id = None
    db.session.add(timeslot)
    db.session.commit()
    flash("Reservation cancelled.")
    return redirect(request.referrer)

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
