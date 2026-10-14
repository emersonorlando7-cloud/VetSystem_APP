from flask import Flask
app = Flask(__name__)

@app.route("/")
def inicio():
    return "¡Hola! La aplicación de la veterinaria está corriendo con éxito 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)