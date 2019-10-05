from flask import *
from app import app, db
from flask_login import *
from werkzeug.urls import *
from datetime import *
from app.forms import LoginForm, PatientRegistrationForm, DoctorRegistrationForm
from app.models import Patient, Doctor, PatientHistory

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# @app.route('/home')
# def home():
@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('home'))

    form_patient = LoginForm()
    form_doctor = LoginForm()

    return render_template('login.html', form_patient=form_patient, form_doctor=form_doctor)

@app.route('/login_doctor', methods=['POST', 'GET'])
def login_doctor():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form_doctor = LoginForm()

    if form_doctor.validate_on_submit():
        doctor = Doctor.query.filer_by(email=form_doctor.email.data).first()

        if doctor and doctor.check_password(password=form_doctor.password.data):
            login_user(doctor)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check mail and password')

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

    if form_patient.validate_on_submit():
        patient = Patient.query.filer_by(email=form_patient.email.data).first()

        if patient and patient.check_password(password=form_patient.password.data):
            login_user(patient)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check mail and password')

@app.route('/register',methods=['GET'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for('home'))

    form_patient = PatientRegistrationForm()
    form_doctor = DoctorRegistrationForm()

    return render_template('register.html', form_patient=form_patient, form_doctor=form_doctor)

@app.route('register_patient', methods = ['GET','POST'])
def register_patient():
    form_patient = PatientRegistrationForm

    if form_patient.validate_on_submit():
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
     
    if form_doctor.validate_on_submit():
        doctor = Doctor(name = form_doctor.name.data, email = form_doctor.email.data,
                         location = form_doctor.location.data, degree = form_doctor.degree.data,
                         specialisation = form_doctor.specialisation.data)
        doctor.set_password(form_doctor.password.data)

        db.session.add(doctor)
        db.session.commit()
    
    else:
        flash("error in signing up")
        
    return redirect(url_for('home'))


@app.route('/home')
@login_required
def home():


@app.route('/permissions')
@login_required
def permissions():

@app.route('/add_patient_data')
@login_required
def add_patient_data():
    if current_user.role == 'p':
        return redirect(url_for('home'))

    elif current_user.role != 'd':
        return redirect(url_for('home'))

@app.route('/patient_history')
@login_required
def add_patient_data():
    if current_user.role == 'p':
        return redirect(url_for('home'))

    elif current_user.role != 'd':
        return redirect(url_for('home'))

