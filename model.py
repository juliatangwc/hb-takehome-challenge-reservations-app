"""Models for reservation app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    timeslot = db.relationship('Timeslot', back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Timeslot(db.Model):
    """A timeslot."""

    __tablename__ = 'timeslots'

    timeslot_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    date = db.Column(db.DateTime)
    time = db.Column(db.DateTime)                   
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship('User', back_populates="timeslot")

    def __repr__(self):
        return f'<Timeslot date={self.date} time={self.time} user_id={self.user_id}>'


def connect_to_db(flask_app, db_uri="postgresql:///reservations", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
