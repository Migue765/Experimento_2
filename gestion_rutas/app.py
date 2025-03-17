from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"mensaje": "Pong!"}), 200


@app.route("/update-route", methods=["POST"])
def procesar_compra():
    return jsonify({"ruta actualizada correctamente": True}), 200  # 200 es el código de estado HTTP para "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4043)
