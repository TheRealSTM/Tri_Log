from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_visited = db.Column(db.DateTime, default=datetime.utcnow)
    swim_workouts = db.relationship('WorkoutSwim', backref='user')
    bike_workouts = db.relationship('WorkoutBike', backref='user')
    run_workouts = db.relationship('WorkoutRun', backref='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class WorkoutSwim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    distance = db.Column(db.Float)
    duration = db.Column(db.Float)
    pace = db.Column(db.String(5))
    stroke_rate = db.Column(db.Integer)
    comments = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Swim Workout {}>'.format(self.user_id)


class WorkoutBike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    distance = db.Column(db.Float)
    duration = db.Column(db.Float)
    pace =  db.Column(db.String(5))
    heart_rate = db.Column(db.Integer)
    watts = db.Column(db.Float)
    comments = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Bike Workout {}>'.format(self.user_id)

class WorkoutRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    distance = db.Column(db.Float)
    duration = db.Column(db.Float)
    pace =  db.Column(db.String(5))
    heart_rate = db.Column(db.Integer)
    comments = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Run Workout {}>'.format(self.user_id)
