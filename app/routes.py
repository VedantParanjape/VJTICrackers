from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_login import login_required, current_user, login_user, logout_user
from datetime import datetime
from app.forms import LoginForm, PatientRegistrationForm, DoctorRegistrationForm, AddPatientHistory, AddOtp
from app.models import Patient, Doctor, PatientHistory
import pyotp
from functools import wraps
from sqlalchemy.exc import IntegrityError

def patient_required(function):
    @wraps(function)
    def is_patient(*args, **kwargs):
        if current_user.role == 'p':
            return True

        else:
            return False
    return is_patient

def doctor_required(function):
    @wraps(function)
    def is_doctor(*args, **kwargs):
        if current_user.role == 'd':
            return True

        else:
            return False
    return is_doctor

@app.route('/', methods=['GET'])
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form_patient = LoginForm()
    form_doctor = LoginForm()

    return render_template('login.html', form_patient=form_patient, form_doctor=form_doctor)

@app.route('/login_doctor', methods=['POST', 'GET'])
def login_doctor():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form_doctor = LoginForm()

    if 1 or form_doctor.validate_on_submit():
        doctor = Doctor.query.filter_by(email=form_doctor.email.data).first()

        if doctor and doctor.check_password(password=form_doctor.password.data):
            login_user(doctor)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
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

@app.route('/login_patient', methods=['POST', 'GET'])
def login_patient():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form_patient = LoginForm()

    if  1 or form_patient.validate_on_submit():
        patient = Patient.query.filter_by(email=form_patient.email.data).first()

        if patient and patient.check_password(password=form_patient.password.data):
            login_user(patient)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check mail and password')
            return redirect(url_for('login'))

    return redirect(url_for('login'))

@app.route('/register',methods=['GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form_patient = PatientRegistrationForm()
    form_doctor = DoctorRegistrationForm()

    return render_template('register.html', form_patient=form_patient, form_doctor=form_doctor)

@app.route('/register_patient', methods = ['GET','POST'])
def register_patient():
    form_patient = PatientRegistrationForm()

    if 1 or form_patient.validate_on_submit():
        patient = Patient(name = form_patient.data, email = form_patient.email.data, 
                          age = form_patient.age.data, gender = form_patient.gender.data,
                          height = form_patient.height.data, weight = form_patient.weight.data,
                          bloodgroup = form_patient.bloodgroup.data, location = form_patient.location.data)
        patient.set_password(form_patient.password.data)

        db.session.add(patient)
        db.session.commit()
    
    else:
        flash("error in signing up")

    return redirect(url_for('home'))    

@app.route('/register_doctor', methods = ['GET', 'POST'])
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
        return flash("Otp generation failed, Refresh to Try Again")

    return render_template('generate_otp.html', otp=otp)

@app.route('/add_patient_data')
@login_required
# @doctor_required
def add_patient_data():
    patient_history = AddPatientHistory()

    if request.method == 'GET':
        return render_template('add_patient_data.html', patient_history=patient_history)

    patient_t = Patient.query.filter_by(otp = patient_history.otp_add.data)

    if patient_id:
        p_history = PatientHistory(patient_id=patient_t.id, 
                                   symptoms=patient_history.symptoms.data, 
                                   diagnosis=patient_history.diagnosis.data,
                                   treatment=patient_history.treatment.data)
        
        return redirect('view_patient_history')
    else:
        flash("Error, Try again")

    
    

@app.route('/view_patient_history')
@login_required
# @doctor_required    
def view_patient_history():
    otpform = AddOtp()

    if request.method == 'GET':
        return render_template('validate_otp.html')

    patient = Patient.query.filter_by(otp = otpform.otp_verify.data).first()

    if patient:
        return render_template('patient_history.html', patienthistory=PatientHistory.query.filter_by(patient_id=patient.id).all())
