from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
import json


def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 401
    return wrapper

def roles_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user=get_jwt_identity()
                user_roles =current_user.get("role")
                print(user_roles)
                print(role)
                if user_roles == role:
                    return fn(*args, **kwargs)
                return jsonify({"error":"Acceso no autorizado"}),403
            except Exception as e:
                return jsonify({"error": str(e)}), 401
        return wrapper
    return decorator