from flask import render_template, flash, redirect, url_for, request
from app import app, db, data
from flask_login import login_required, current_user, login_user, logout_user
from datetime import datetime
from app.forms import LoginForm, PatientRegistrationForm, DoctorRegistrationForm, AddPatientHistory, AddOtp, Predict_
from app.models import Patient, Doctor, PatientHistory
import pyotp
from functools import wraps
from sqlalchemy.exc import IntegrityError
import csv
import numpy as np
import pickle
import matplotlib.pyplot as plot, mpld3

@app.route('/', methods=['GET'])
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form_patient = LoginForm()
    form_doctor = LoginForm()

    return render_template('login.html', form_patient=form_patient, form_doctor=form_doctor, title='Login')

@app.route('/login_doctor', methods=['POST'])
def login_doctor():
    if current_user.is_authenticated:
        print("redirected from login doctor")
        return redirect(url_for('home'))

    form_doctor = LoginForm()

    if 1 or form_doctor.validate_on_submit():
        doctor = Doctor.query.filter_by(email=form_doctor.email.data).first()
        # print(doctor.role)
        if doctor and doctor.check_password(password=form_doctor.password.data):
            print("before doctor login")
            login_user(doctor)
            print("user logged in as doctor")
            data.set_type('doctor')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            print('Login unsuccessful. Please check mail and password')
            flash('Login unsuccessful. Please check mail and password')
            return redirect(url_for('login'))

    return redirect(url_for('login'))
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data).first()
    #     if user and bcrypt.check_password_hash(user.password, form.password.data):
    #         login_user(user, remember=form.remember.data)
    #         next_page = request.args.get('next')
    #         return redirect(next_page) if next_page else redirect(url_for('home'))
    #     else:
    #         flash('Login Unsuccessful. Please check email and password', 'danger')

@app.route('/login_patient', methods=['POST'])
def login_patient():
    if current_user.is_authenticated:
        print("redirected from login patient")
        return redirect(url_for('home'))

    form_patient = LoginForm()
    
    if  1 or form_patient.validate_on_submit():
        patient = Patient.query.filter_by(email=form_patient.email.data).first()
        
        if patient and patient.check_password(password=form_patient.password.data):
            print("before patient login")
            login_user(patient)
            print("user logged in as patient")
            data.set_type('patient')
            next_page = request.args.get('next')
            
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            print('Login unsuccessful. Please check mail and password')
            flash('Login unsuccessful. Please check mail and password')
            return redirect(url_for('login'))

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    data.set_type('nil')
    logout_user()
    return redirect(url_for('home'))

@app.route('/register',methods=['GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form_patient = PatientRegistrationForm()
    form_doctor = DoctorRegistrationForm()

    return render_template('register.html', form_patient=form_patient, form_doctor=form_doctor, title="Sign Up")

@app.route('/register_patient', methods = ['POST'])
def register_patient():
    form_patient = PatientRegistrationForm()

    if 1 or form_patient.validate_on_submit():
        patient = Patient(name = form_patient.name.data, email = form_patient.email.data, 
                          age = form_patient.age.data, gender = form_patient.gender.data,
                          height = form_patient.height.data, weight = form_patient.weight.data,
                          bloodgroup = form_patient.bloodgroup.data, location = form_patient.location.data)
        patient.set_password(form_patient.password.data)

        db.session.add(patient)
        db.session.commit()
    
    else:
        flash("error in signing up")

    return redirect(url_for('home'))    

@app.route('/register_doctor', methods = ['POST'])
def register_doctor():
    form_doctor = DoctorRegistrationForm()
     
    if 1 or form_doctor.validate_on_submit():
        doctor = Doctor(name = form_doctor.name.data, email = form_doctor.email.data,
                         location = form_doctor.location.data, degree = form_doctor.degree.data,
                         specialisation = form_doctor.specialisation.data)
        doctor.set_password(form_doctor.password.data)

        db.session.add(doctor)
        db.session.commit()
    
    else:
        flash("error in signing up")

    return redirect(url_for('home'))



@app.route('/generate_otp')
@login_required
# @patient_required
def generate_otp():
    otp = pyotp.random_base32()
    
    current_user.otp = otp
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print("otp generation failed")
        return flash("Otp generation failed, Refresh to Try Again")

    return render_template('generate_otp.html', otp=otp, title="OTP")

@app.route('/add_patient_data', methods=['GET', 'POST'])
@login_required
# @doctor_required
def add_patient_data():
    patient_history = AddPatientHistory()

    if request.method == 'GET':
        return render_template('analysis.html', patient_history=patient_history, title="Add Patient Data")

    patient_t = Patient.query.filter_by(otp = patient_history.otp_add.data).first()
    print(patient_t)
    if patient_t:
        p_history = PatientHistory(patient_id=patient_t.id,
                                   symptoms=patient_history.symptoms.data, 
                                   diagnosis=patient_history.diagnosis.data,
                                   treatment=patient_history.treatment.data)
        db.session.add(p_history)
        db.session.commit()
        print('validated')
        return redirect('view_patient_history')
    else:
        print("error, try again")
        flash("Error, Try again")

@app.route('/view_patient_history', methods=['GET','POST'])
@login_required
# @doctor_required    
def view_patient_history():
    otpform = AddOtp()

    if request.method == 'GET':
        return render_template('validate_otp.html', otpform=otpform, title='Validate OTP')

    patient = Patient.query.filter_by(otp = otpform.otp_verify.data).first()
    # print(patient.name, patient.otp)
    if patient:
        print('inside patient if', patient)
        patient_history = PatientHistory.query.filter_by(patient_id=patient.id).all()
        print(patient_history)
        return render_template('patient_history.html', title='Patient History',patient=patient, patient_history=patient_history)
    else:
        return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    patient_history = PatientHistory.query.filter_by(patient_id=current_user.id).all()
    return render_template('profile.html', title='Profile', patient_history=patient_history)

@app.route('/predict',methods=['POST', 'GET'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    predict_ = Predict_()
    model = pickle.load( open('model.pkl','rb'))

    if request.method == 'GET':
        return render_template('predict.html', predict_=predict_, prediction_text = "")
    
    Location = predict_.location.data

    f = open('app/pm_data.csv', 'r')
    reader = csv.reader(f)
    loc = {}

    for row in reader:
        loc[row[0]] = row[1]

    pm = loc[str(Location)]
    print(pm, Location)
    prediction = model.predict([[float(pm)]])

    output = round(prediction[0][0], 2)

    return render_template('predict.html', predict_=predict_, prediction_text=output)