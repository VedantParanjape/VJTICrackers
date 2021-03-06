from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from datetime import datetime
from app import data
class Patient(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(2))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    bloodgroup = db.Column(db.String(4))
    location = db.Column(db.String(50))
    # patienthistory = db.relationship('PatientHistory', backref='history', lazy='True')
    role = db.Column(db.String(1), default='p')
    otp = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return '<Patient {}>'.format(self.name)

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Doctor(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    degree = db.Column(db.String(20), nullable=False)
    specialisation = db.Column(db.String(30))
    role = db.Column(db.String(1), default='d')
    # doctorhistory = db.relationship('PatientHistory', backref='history', lazy='dynamic')
    # degreeoofpath = db.Column(db.String(30), nullable=False)
    
    def __repr__(self):
        return '<Doctor {}>'.format(self.name)
    
    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class PatientHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    patient_id = db.Column(db.Integer, nullable=False)
    # doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    symptoms = db.Column(db.String(200))
    diagnosis = db.Column(db.String(200))
    treatment = db.Column(db.String(200))
    
    def __repr__(self):
        return '<PatientHistory {} {} {} {}>'.format(self.id, self.symptoms, self.diagnosis, self.treatment)

@login.user_loader
def load_patient(id):
    print("userloader called", data.check_type())
    if data.check_type() == 'doctor':
        print("userloader: doctor")
        return Doctor.query.get(int(id))
    
    elif data.check_type() == 'patient':
        print("userloader: patient")
        return Patient.query.get(int(id))


