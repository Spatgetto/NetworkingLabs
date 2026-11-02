from flask import Flask, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///network.db"
db = SQLAlchemy(app)

class ValidationError(Exception):
    pass

class Device(db.Model):
    device_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    mgmt_address = db.Column(db.String(120), nullable=False)
    vendor = db.Column(db.String(64), nullable=False)

    def get_url(self):
        return url_for('get_device', device_id=self.device_id, _external=True)

    def export_data(self):
        return {
            'device_id': self.device_id,
            'name': self.name,
            'mgmt_address': self.mgmt_address,
            'vendor': self.vendor,
        }

    def import_data(self, data):
        try:
            self.name = data['name']
            self.mgmt_address = data['mgmt_address']
            self.vendor = data['vendor']
        except KeyError as e:
            raise ValidationError(f'Missing field: {e.args[0]}')
        return self

@app.route('/devices/', methods=['GET'])
def get_devices():
    devices = Device.query.all()
    return jsonify([device.get_url() for device in devices])
@app.route('/devices/', methods=['POST'])
def create_device():
    device = Device()
    device.import_data(request.json)
    db.session.add(device)
    db.session.commit()
    return jsonify({}), 201, {'Location': device.get_url()}

@app.route('/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    return jsonify(Device.query.get_or_404(device_id).export_data())
@app.route('/devices/<int:device_id>', methods=['PUT'])
def edit_device(device_id):
    device = Device.query.get_or_404(device_id)
    device.import_data(request.json)
    db.session.add(device)
    db.session.commit()
    return jsonify({})
@app.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return jsonify({}), 204

# Initialize database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
