from flask_wtf import *
from flask_wtf.file import *
from flask_login import current_user
from wtforms import *
from wtforms.validators import *
from flaskblog.models import User

class PatientRegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    age = IntegerField('Age', validators=[DataRequired(), Length(min=0, max=100)])
    gender = StringField('Gender', validators=[DataRequired()])
    height = IntegerField('Height', validators=[DataRequired(), Length(min=15, max=400)])
    weight = IntegerField('Weight', validators=[DataRequired(), Length(min=1, max=600)])
    bloodgroup = StringField('Blood Group', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
       
    #submit = SubmitField('Sign Up')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('That username is taken. Please choose a different one.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email is taken. Please choose a different one.')

class DoctorRegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    degree = StringField('Degree', validators=[DataRequired()])
    specialisation = StringField('Specialisation', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    picture = FileField('Degree Proof', validators=[FileAllowed(['jpg', 'png'])])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

class AddPatientHistory(FlaskForm):
    symptoms = StringField('Symptoms',
                           validators=[DataRequired(), Length(min=2, max=200)]) 
    diagnosis = StringField('Diagnosis',
                           validators=[DataRequired(), Length(min=2, max=200)])
    treatment = StringField('Treatment',
                           validators=[DataRequired(), Length(min=2, max=200)])
    otp_add = StringField('OTP', validators=[DataRequired])

class AddOtp(FlaskForm):
    otp_verify = StringField('OTP', validators=[DataRequired])

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
