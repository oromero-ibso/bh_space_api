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

@app.route('/api/products', methods=['GET'])
def get_paginated_products():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"message": "Unauthorized", "status": "error"}), 401

    token = auth_header.split(" ")[1]
    if token != VALID_TOKEN:
        return jsonify({"message": "Unauthorized", "status": "error"}), 401

    # Parámetros de paginación
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 600))  # default 600
        limit = min(limit, 1000)  # máximo 1000 por seguridad
    except ValueError:
        return jsonify({"message": "Invalid pagination params"}), 400

    start = (page - 1) * limit
    end = start + limit
    data = productos[start:end]

    return jsonify({
        "page": page,
        "limit": limit,
        "total": len(productos),
        "pages": (len(productos) + limit - 1) // limit,  # redondeo hacia arriba
        "data": data
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
