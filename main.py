from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
from os import getenv  # Necesario para Railway

app = Flask(__name__)
CORS(app)

GPS_FILE = "data.json"
IMAGEN_FILE = "ultima.jpg"

# Crear archivo si no existe
if not os.path.exists(GPS_FILE):
    with open(GPS_FILE, "w") as f:
        json.dump([], f)

@app.route("/api/gps", methods=["POST"])
def recibir_datos():
    # Si se envía imagen desde el ESP32-CAM
    if 'image' in request.files:
        image = request.files['image']
        image.save(IMAGEN_FILE)
        print("✅ Imagen recibida y guardada")
        return jsonify({"status": "imagen guardada"}), 200

    # Si se envía JSON desde el módulo GPS
    try:
        data = request.get_json()
        print("Datos GPS recibidos:", data)

        nuevo_dato = {
            "device_id": data.get("device_id", ""),
            "timestamp": data.get("timestamp", [""])[0],
            "lat": data.get("lat", [0])[0],
            "lon": data.get("long", [0])[0]
        }

        with open(GPS_FILE, "r+") as f:
            contenido = json.load(f)
            contenido.append(nuevo_dato)
            f.seek(0)
            json.dump(contenido, f, indent=2)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/ultima.jpg")
def ultima_imagen():
    return send_from_directory(".", IMAGEN_FILE)

@app.route("/borrar", methods=["DELETE"])
def borrar_puntos():
    try:
        with open(GPS_FILE, "w") as f:
            json.dump([], f)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/data.json")
def obtener_datos():
    return send_from_directory(".", GPS_FILE)

@app.route("/")
def presentacion():
    return send_from_directory(".", "Presentacion.html")

@app.route("/mapa")
def mapa():
    return send_from_directory(".", "mapa.html")

@app.route("/estilos.css")
def estilos_mapa():
    return send_from_directory(".", "estilos.css")

@app.route("/mapa.js")
def script_mapa():
    return send_from_directory(".", "mapa.js")

@app.route("/estilop.css")
def estilos_presentacion():
    return send_from_directory(".", "estiloP.css")

@app.route("/script.js")
def script_presentacion():
    return send_from_directory(".", "Script.js")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(getenv("PORT", 5000)))

