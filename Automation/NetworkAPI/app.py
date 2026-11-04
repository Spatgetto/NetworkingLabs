
import ipaddress
import os

from datetime import datetime, timezone
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Database setup

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///network.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Association Table: Devices <-> Device Groups

device_group_association = db.Table(
    "device_group_association",

    db.Column(
        "device_id",
        db.Integer,
        db.ForeignKey("device.device_id"),
        primary_key=True
    ),
    db.Column(
        "group_id",
        db.Integer,
        db.ForeignKey("device_group.group_id"),
        primary_key=True
    )
)

class Device(db.Model):
    device_id = db.Column(
        db.Integer, 
        primary_key=True
    )
    name = db.Column(
        db.String(80), 
        nullable=False
    )
    mgmt_address = db.Column(
        db.String(64), 
        nullable=False,
        unique=True
    )
    vendor = db.Column(
        db.String(64), 
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )   

    groups = db.relationship(
        "DeviceGroup",
        secondary=device_group_association,
        back_populates="devices"
    )

class DeviceGroup(db.Model):
    group_id = db.Column(
        db.Integer, 
        primary_key=True
    )
    name = db.Column(
        db.String(80), 
        nullable=False, 
        unique=True
    )
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    devices = db.relationship(
        "Device",
        secondary=device_group_association,
        back_populates="groups"
    )

with app.app_context():
    db.create_all()
