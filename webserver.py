from app import app
from app import db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Patient': Patient, 'Doctor': Doctor}

