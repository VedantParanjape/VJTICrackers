from app import app
from app import db
from app.models import Patient, Doctor, PatientHistory

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Patient': Patient, 'Doctor': Doctor, 'PatientHistory': PatientHistory}

if __name__ == "__main__":
    app.run(debug=True)