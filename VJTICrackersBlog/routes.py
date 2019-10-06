from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from VJTICrackersBlog import app, db, bcrypt
from VJTICrackersBlog.forms import RegistrationForm, LoginForm
from VJTICrackersBlog.models import User
from flask_login import login_user, current_user, logout_user, login_required
import numpy as np
import csv

# from flask import Flask, request, jsonify
import pickle

class Predict_(FlaskForm):
    location = StringField('Location', validators=[DataRequired()])

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template("signup.html")
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    # form = RegistrationForm()
    # if form.validate_on_submit():
    #     hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    #     user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    #     db.session.add(user)
    #     db.session.commit()
    #     flash('Your account has been created! You are now able to log in', 'success')
    #     return redirect(url_for('login'))
    # return render_template('register.html', title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/profile")
#zdg
def profile():
    return render_template('profile.html', title='Profile', case='pat_profile')

# @app.route("/verify")
# def verify():
#     return render_template('verify_otp.html')

@app.route('/predict',methods=['POST', 'GET'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    predict_ = Predict_()

    if flask.request.methods=='GET':
        return render_template('predict.html', predict_=predict_, prediction_text = "")
    
    Location = predict_.location.data

    f = open('pm_data.csv', 'r')
    reader = csv.reader(f)

    for row in reader:
        print(row)

    int_features = 3

    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    