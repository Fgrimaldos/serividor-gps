from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
from os import getenv  # ← necesario para Railway

app = Flask(__name__)
CORS(app)

GPS_FILE = "data.json"

# Crear archivo vacío si no existe
if not os.path.exists(GPS_FILE):
    with open(GPS_FILE, "w") as f:
        json.dump([], f)

@app.route("/api/gps", methods=["POST"])
def recibir_datos():
    try:
        data = request.get_json()
        print("📥 Datos recibidos:", data)

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

@app.route("/api/clear", methods=["POST"])
def borrar_datos():
    try:
        with open(GPS_FILE, "w") as f:
            json.dump([], f)
        print("🗑️ Datos GPS eliminados.")
        return jsonify({"status": "datos eliminados"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/data.json")
def obtener_datos():
    return send_from_directory('.', GPS_FILE)

@app.route("/")
def index():
    return send_from_directory('.', "mapa.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(getenv("PORT", 5000)))

