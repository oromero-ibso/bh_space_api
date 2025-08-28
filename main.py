from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Token válido
VALID_TOKEN = "ceEpOIjcVcHpPThviYYFw"

BASE_DIR = os.path.dirname(__file__)
with open(os.path.join(BASE_DIR, "data", "productos.json"), "r", encoding="utf-8") as f:
    productos = json.load(f)

@app.route('/')
def root():
    return "Home"

@app.route('/api/all_products', methods=['GET'])
def get_data():
    # Leer header Authorization
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Unauthorized", "status": "error"}), 401

    token = auth_header.split(" ")[1]

    if token != VALID_TOKEN:
        return jsonify({"message": "Unauthorized", "status": "error"}), 401

    # Devolver el JSON cargado
    return jsonify(productos), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
