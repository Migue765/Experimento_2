from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SERVICES = {
    "rutas": "http://rutas:4043",
    "login": "http://login:5000",
}


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"mensaje": "Pong!"}), 200


@app.route("/api/<servicio>/<path:endpoint>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy(servicio, endpoint):
    token = request.headers.get("Authorization")
    if not token and servicio != "login":
        return jsonify({"error": "Token no proporcionado"}), 401
    elif servicio == "login" and endpoint == "generate_token":
        url = f"{SERVICES[servicio]}/{endpoint}"
        response = requests.post(url, json=request.json)
        return jsonify(response.json()), response.status_code

    validation_response = requests.post(f"{SERVICES['login']}/validate_token", headers={"Authorization": token})
    print(validation_response)
    if validation_response.status_code != 200:
        return jsonify({"error": "Token inválido"}), 401

    validation_data = validation_response.json()
    if not validation_data.get("valid") or not validation_data.get("admin"):
        return jsonify({"error": "No autorizado"}), 403

    if servicio not in SERVICES:
        return jsonify({"error": "Servicio no encontrado: " + servicio}), 404

    url = f"{SERVICES[servicio]}/{endpoint}"
    if request.method == "POST":
        response = requests.post(url, json=request.json)
    elif request.method == "PUT":
        response = requests.put(url, json=request.json)
    elif request.method == "DELETE":
        response = requests.delete(url, json=request.json)
    else:  # GETs
        response = requests.get(url, params=request.args)

    return jsonify(response.json()), response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8020)
