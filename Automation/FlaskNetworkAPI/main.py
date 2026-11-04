"""Network device inventory REST API (Flask + SQLAlchemy)."""
import ipaddress
import os

from flask import Flask, jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///network.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class ValidationError(Exception):
    """Raised when client input is invalid (maps to HTTP 400)."""


# --------------------------------------------------------------------------
# Validation helpers
# --------------------------------------------------------------------------
def clean_str(data, field, max_len):
    value = data.get(field)
    if value is None:
        raise ValidationError(f"Missing field: {field}")
    if not isinstance(value, str):
        raise ValidationError(f"Field '{field}' must be a string")
    value = value.strip()
    if not value:
        raise ValidationError(f"Field '{field}' must not be empty")
    if len(value) > max_len:
        raise ValidationError(f"Field '{field}' must be at most {max_len} characters")
    return value


def clean_mgmt_address(raw):
    """Validate and normalize a management IP (IPv4 or IPv6)."""
    try:
        ip = ipaddress.ip_address(raw)
    except ValueError:
        raise ValidationError(f"'{raw}' is not a valid IPv4/IPv6 address")
    if ip.is_unspecified or ip.is_loopback or ip.is_multicast:
        raise ValidationError(
            f"'{raw}' cannot be used as a management address "
            "(unspecified, loopback and multicast are not allowed)"
        )
    # str(ip) normalizes the form, e.g. 2001:0DB8::0001 -> 2001:db8::1
    return str(ip)


def get_json_object():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")
    return data


# --------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------
class Device(db.Model):
    device_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    # 64 chars covers IPv6 with a zone id; unique so one IP maps to one device
    mgmt_address = db.Column(db.String(64), nullable=False, unique=True)
    vendor = db.Column(db.String(64), nullable=False)

    def get_url(self):
        return url_for("get_device", device_id=self.device_id, _external=True)

    def export_data(self):
        return {
            "device_id": self.device_id,
            "name": self.name,
            "mgmt_address": self.mgmt_address,
            "vendor": self.vendor,
            "ip_version": ipaddress.ip_address(self.mgmt_address).version,
            "url": self.get_url(),
        }

    def import_data(self, data, partial=False):
        """Validate `data` and apply it. partial=True (PATCH) allows missing fields."""
        fields = {
            "name": lambda d: clean_str(d, "name", 80),
            "mgmt_address": lambda d: clean_mgmt_address(clean_str(d, "mgmt_address", 64)),
            "vendor": lambda d: clean_str(d, "vendor", 64),
        }
        updates = {}
        for field, cleaner in fields.items():
            if partial and field not in data:
                continue
            updates[field] = cleaner(data)
        # Only touch the model once everything validated
        for field, value in updates.items():
            setattr(self, field, value)
        return self


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------
@app.route("/devices/", methods=["GET"])
def get_devices():
    """List device URLs. Optional filters: ?vendor=cisco  ?subnet=10.0.0.0/24"""
    query = db.select(Device).order_by(Device.device_id)

    vendor = request.args.get("vendor")
    if vendor:
        query = query.where(func.lower(Device.vendor) == vendor.strip().lower())

    devices = db.session.scalars(query).all()

    subnet = request.args.get("subnet")
    if subnet:
        try:
            network = ipaddress.ip_network(subnet.strip(), strict=False)
        except ValueError:
            raise ValidationError(f"'{subnet}' is not a valid network (e.g. 10.0.0.0/24)")
        # Membership across IP versions is simply False, so mixed v4/v6 is safe
        devices = [d for d in devices if ipaddress.ip_address(d.mgmt_address) in network]

    return jsonify([d.get_url() for d in devices])


@app.route("/devices/", methods=["POST"])
def create_device():
    device = Device().import_data(get_json_object())
    db.session.add(device)
    db.session.commit()
    return jsonify(device.export_data()), 201, {"Location": device.get_url()}


@app.route("/devices/<int:device_id>", methods=["GET"])
def get_device(device_id):
    return jsonify(db.get_or_404(Device, device_id).export_data())


@app.route("/devices/<int:device_id>", methods=["PUT"])
def edit_device(device_id):
    """Full replace: all fields required."""
    device = db.get_or_404(Device, device_id)
    device.import_data(get_json_object())
    db.session.commit()
    return jsonify(device.export_data())


@app.route("/devices/<int:device_id>", methods=["PATCH"])
def patch_device(device_id):
    """Partial update: only supplied fields change."""
    device = db.get_or_404(Device, device_id)
    device.import_data(get_json_object(), partial=True)
    db.session.commit()
    return jsonify(device.export_data())


@app.route("/devices/<int:device_id>", methods=["DELETE"])
def delete_device(device_id):
    device = db.get_or_404(Device, device_id)
    db.session.delete(device)
    db.session.commit()
    return "", 204  # 204 must not carry a body


# --------------------------------------------------------------------------
# Error handlers (consistent JSON errors)
# --------------------------------------------------------------------------
@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({"error": "validation_error", "message": str(e)}), 400


@app.errorhandler(IntegrityError)
def handle_integrity_error(e):
    db.session.rollback()
    return jsonify({
        "error": "conflict",
        "message": "A device with that management address already exists",
    }), 409


@app.errorhandler(HTTPException)
def handle_http_error(e):
    return jsonify({"error": e.name.lower().replace(" ", "_"), "message": e.description}), e.code


# --------------------------------------------------------------------------
# Startup
# --------------------------------------------------------------------------
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # The Werkzeug debugger allows remote code execution, so never combine
    # debug=True with host 0.0.0.0. Opt in explicitly via env vars instead.
    app.run(
        host=os.environ.get("FLASK_HOST", "127.0.0.1"),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )