#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/events')
def get_events():
    events = Event.query.all()
    return jsonify([{"id": e.id, "name": e.name, "location": e.location} for e in events]), 200

@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = Event.query.filter_by(id=id).first()
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify([{"id": s.id, "title": s.title, "start_time": s.start_time.isoformat()} for s in event.sessions]), 200

@app.route('/speakers')
def get_speakers():
    speakers = Speaker.query.all()
    return jsonify([{"id": s.id, "name": s.name} for s in speakers]), 200

@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = Speaker.query.filter_by(id=id).first()
    if not speaker:
        return jsonify({"error": "Speaker not found"}), 404
    bio_text = speaker.bio.bio_text if speaker.bio else "No bio available"
    return jsonify({"id": speaker.id, "name": speaker.name, "bio_text": bio_text}), 200

@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = Session.query.filter_by(id=id).first()
    if not session:
        return jsonify({"error": "Session not found"}), 404
    return jsonify([{
        "id": sp.id,
        "name": sp.name,
        "bio_text": sp.bio.bio_text if sp.bio else "No bio available"
    } for sp in session.speakers]), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)