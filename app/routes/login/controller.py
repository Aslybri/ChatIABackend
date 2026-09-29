from flask import ( jsonify, request)
from .service import login_service
def login_controller():
    data = request.get_json() or {}
    if not data:
        return jsonify({
            'message': 'Faltan datos'
        }),400
    email = data.get('email')
    password = data.get('password')
    result = login_service(email, password)
    return jsonify(result),200