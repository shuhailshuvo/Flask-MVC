from flask import request, jsonify


def send(data, message, status=200):
    return jsonify({"data": data, "message": message}), status
