from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, TextAreaField, PasswordField, BooleanField, SubmitField # Classes with wtforms
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User




class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SwimForm(FlaskForm):
    distance = FloatField('Distance')
    duration = FloatField('Duration (in min)')
    pace = StringField('Pace')
    stroke_rate = IntegerField('Stroke Rate')
    body = TextAreaField('Comments')
    submit = SubmitField('Submit Workout')

class BikeForm(FlaskForm):
    distance = FloatField('Distance')
    duration = FloatField('Duration (in min)')
    pace = StringField('Pace')
    heart_rate = IntegerField('Heart Rate')
    watts = FloatField('Watts')
    body = TextAreaField('Comments')
    submit = SubmitField('Submit Workout')


class RunForm(FlaskForm):
    distance = FloatField('Distance')
    duration = FloatField('Duration (in min)')
    pace = StringField('Pace')
    heart_rate = IntegerField('Heart Rate')
    body = TextAreaField('Comments')
    submit = SubmitField('Submit Workout')
