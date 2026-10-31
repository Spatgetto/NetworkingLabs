from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///network.db"
db = SQLAlchemy(app)

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(120), index=True)
    vendor = db.Column(db.String(40))
    ipv4 = db.Column(db.String(15))
    def __init__(self, hostname, vendor, ipv4):
        self.hostname = hostname
        self.vendor = vendor
        self.ipv4 = ipv4
    def __repr__(self):
        return '<Device %r>' % self.hostname
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        r1 = Device('R1', 'Cisco', '10.99.99.10')
        r2 = Device('R2', 'Cisco', '10.99.99.20')
        r3 = Device('R3', 'Cisco', '10.99.99.30')

        db.session.add_all([r1, r2, r3])
        db.session.commit()

        devices = Device.query.all()

        for device in devices:
            print(device.hostname, device.vendor, device.ipv4)