import os
from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "192.168.56.13")
DB_USER = os.environ.get("DB_USER", "app_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "AppPass123!")
DB_NAME = os.environ.get("DB_NAME", "vet_clinic_db")

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/inicio")
def inicio():
    return render_template("Inicio.html")

@app.route("/pacientes")
def pacientes():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM owners")
        owners = cursor.fetchall()
    connection.close()
    return render_template("pacientes.html", owners=owners)

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]

        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO owners (name, phone, email, address) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, phone, email, address))
            connection.commit()
        connection.close()
        return redirect(url_for("pacientes"))
    return render_template("index.html")

@app.route("/usuarios")
def usuarios():
    return render_template("usuarios.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
