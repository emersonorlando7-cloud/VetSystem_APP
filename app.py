from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import socket

app = Flask(__name__)
app.secret_key = 'clave_secreta_muy_segura'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://app_user:AppPass123!@192.168.56.10:3306/vet_clinic_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Owner(db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(255))

class Pet(db.Model):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50))
    breed = db.Column(db.String(50))
    age = db.Column(db.Integer)
    weight = db.Column(db.Numeric(5, 2))

class Consultation(db.Model):
    __tablename__ = 'consultations'
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    reason = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    consultation_date = db.Column(db.DateTime, server_default=db.func.now())

@app.route('/')
def index():
    return redirect(url_for('registrar_paciente'))

@app.route('/registrar', methods=['GET', 'POST'])
def registrar_paciente():
    if request.method == 'POST':
        try:
            owner = Owner(
                name=request.form['owner_name'],
                phone=request.form.get('owner_phone'),
                email=request.form.get('owner_email'),
                address=request.form.get('owner_address')
            )
            db.session.add(owner)
            db.session.flush()

            pet = Pet(
                owner_id=owner.id,
                name=request.form['pet_name'],
                species=request.form.get('pet_species'),
                breed=request.form.get('pet_breed'),
                age=request.form.get('pet_age'),
                weight=request.form.get('pet_weight')
            )
            db.session.add(pet)
            db.session.flush()

            consultation = Consultation(
                pet_id=pet.id,
                reason=request.form['reason'],
                diagnosis=request.form.get('diagnosis')
            )
            db.session.add(consultation)
            db.session.commit()
            flash('Paciente registrado exitosamente!', 'success')
            return redirect(url_for('registrar_paciente'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar: {str(e)}', 'danger')

    hostname = socket.gethostname()
    return render_template('index.html', hostname=hostname)

if __name__ == '__main__':
    app.run(debug=True)
