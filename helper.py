"""CRUD operations."""

from model import db, User, Timeslot, connect_to_db

### for seed.py
def create_timeslots(date, time, user_id=None):
    """Create and return a a new timeslot."""

    timeslot = Timeslot(date=date, time=time, user_id=user_id)
    
    return timeslot

### for server.py
def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def get_user_by_email(email):
    """Check if user with email exists.
        If true, return user. 
        If false, return None."""
    
    return User.query.filter(User.email == email).first()

def check_user_password(email, password):
    """If password entered matches password in databse, return True.
        If password does not match, return False."""
    
    user = User.query.filter(User.email == email).first()

    if user.password == password:
        return user
    else:
        return False

def show_all_reservation(user_id):
    """Return all reservations made by user given user ID."""

    return Timeslot.query.filter(Timeslot.user_id == user_id).all()

def show_available_timeslots(date, start=None, end=None):
    """Return all available timeslots given a date, start and end time"""
    
    if start and end:
        return Timeslot.query.filter(Timeslot.date == date, Timeslot.time>start, Timeslot.time<end, Timeslot.user_id == None).all()
    elif start and not end:
        return Timeslot.query.filter(Timeslot.date == date, Timeslot.time>start, Timeslot.user_id == None).all()
    elif end and not start:
        return Timeslot.query.filter(Timeslot.date == date, Timeslot.time<end, Timeslot.user_id == None).all()
    else:
        return Timeslot.query.filter(Timeslot.date == date, Timeslot.user_id == None).all()

def get_timeslot_by_date_time(date, time):
    """Return a timeslot given a date and time"""

    return Timeslot.query.filter(Timeslot.date == date, Timeslot.time == time).first()
       


if __name__ == '__main__':
    from server import app
    connect_to_db(app)