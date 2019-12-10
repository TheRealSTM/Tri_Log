from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import RegistrationForm, LoginForm, BikeForm, SwimForm, RunForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, WorkoutSwim, WorkoutBike, WorkoutRun
from werkzeug.urls import url_parse
from datetime import datetime as dt

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title = "Home")

@app.route('/about')
def about():
    return render_template("about.html", title = "About")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    swim_data = WorkoutSwim.query.filter_by(user=user)
    bike_data = WorkoutBike.query.filter_by(user=user)
    run_data = WorkoutRun.query.filter_by(user=user)
    return render_template("user.html", user=user, swim_workouts=swim_data,
                           bike_workouts=bike_data, run_workouts=run_data)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_visited = dt.utcnow()
        db.session.commit()



@app.route('/workouts')
@login_required
def workouts():
    return render_template("workouts.html", title = "Select Workout")


@app.route('/swim_workout', methods = ['GET', 'POST'])
@login_required
def swim_workout():
    form = SwimForm()
    if form.validate_on_submit():
        wk_swim = WorkoutSwim(distance=form.distance.data, duration=form.duration.data,
                              pace=form.pace.data, stroke_rate=form.stroke_rate.data,
                              comments=form.body.data, user=current_user)
        db.session.add(wk_swim)
        db.session.commit()
        flash('Congratulations, you have added a swim workout!')
        return redirect(url_for("index"))
    if form.errors:
        app.logger.debug(form.errors)
    return render_template("swim.html", title = "Add Swim Workout", form = form)


@app.route('/bike_workout', methods = ['GET', 'POST'])
@login_required
def bike_workout():
    form = BikeForm()
    if form.validate_on_submit():
        wk_bike =  WorkoutBike(distance=form.distance.data, duration=form.duration.data,
                               pace=form.pace.data, heart_rate=form.heart_rate.data,
                               watts=form.watts.data, comments=form.body.data,
                               user=current_user)
        db.session.add(wk_bike)
        db.session.commit()
        flash('Congratulations, you have added a bike workout!')
        return redirect(url_for("index"))
    return render_template("bike.html", title = "Add Bike Workout", form = form)

@app.route('/run_workout', methods = ['GET', 'POST'])
@login_required
def run_workout():
    form = RunForm()
    if form.validate_on_submit():
        wk_run = WorkoutRun(distance=form.distance.data, duration=form.duration.data,
                            pace=form.pace.data, heart_rate=form.heart_rate.data,
                            comments=form.body.data, user=current_user)
        db.session.add(wk_run)
        db.session.commit()
        flash('Congratulations, you have added a run workout!')
        return redirect(url_for("index"))
    return render_template("run.html", title = "Add Run Workout", form = form)
