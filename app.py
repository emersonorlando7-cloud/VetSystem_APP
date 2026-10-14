import os
from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Configuración de la conexión a la base de datos MySQL (IP de tu servidor db-01)
DB_HOST = os.environ.get("DB_HOST", "192.168.56.13")
DB_USER = os.environ.get("DB_USER", "app_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "AppPass123!")
DB_NAME = os.environ.get("DB_NAME", "vet_clinic_db")

def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

@app.route("/")
def index():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM owners")
        owners = cursor.fetchall()
    connection.close()
    return render_template("index.html", owners=owners)

@app.route("/add", methods=["POST"])
def add_owner():
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

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
