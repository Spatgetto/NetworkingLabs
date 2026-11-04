from datetime import datetime, timezone

from app import db


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

    def export_data(self):
        return {
            "group_id": self.group_id,
            "name": self.name,
            "devices": [
                {
                    "device_id": device.device_id,
                    "name": device.name,
                    "mgmt_address": device.mgmt_address,
                    "vendor": device.vendor
                }
                for device in self.devices
            ]
        }