from flask import Blueprint

devices_bp = Blueprint("devices", __name__)

@devices_bp.route("/", methods=["GET"])
def get_devices():
    return {"message": "List of devices"}