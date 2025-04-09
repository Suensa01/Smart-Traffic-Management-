from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traffic.db'
db = SQLAlchemy(app)

class TrafficData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50))
    vehicle_count = db.Column(db.Integer)
    avg_speed = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    data = TrafficData.query.order_by(TrafficData.timestamp.desc()).limit(10).all()
    return render_template('index.html', data=data)


@app.route('/api/traffic', methods=['POST'])
def receive_data():
    content = request.get_json()
    try:
        new_entry = TrafficData(
            location=content['location'],
            vehicle_count=content['vehicle_count'],
            avg_speed=content['avg_speed']
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'message': 'Data saved successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
