#!/usr/bin/env python3

from app import app
from models import db, Event, Session, Speaker, Bio
import datetime

with app.app_context():
    # Clear all table data
    db.session.execute(db.text('DELETE FROM session_speakers'))
    Bio.query.delete()
    Session.query.delete()
    Speaker.query.delete()
    Event.query.delete()
    db.session.commit()

    # Create Events
    event1 = Event(name="Tech Future Conference", location="New York")
    event2 = Event(name="AI World Summit", location="San Francisco")
    db.session.add_all([event1, event2])
    db.session.commit()

    # Create Sessions
    session1 = Session(title="Building Scalable Web Apps", start_time=datetime.datetime(2023, 9, 15, 10, 0), event=event1)
    session2 = Session(title="Intro to Machine Learning", start_time=datetime.datetime(2023, 9, 15, 14, 0), event=event1)
    session3 = Session(title="The Future of AI Ethics", start_time=datetime.datetime(2023, 10, 20, 11, 0), event=event2)
    db.session.add_all([session1, session2, session3])
    db.session.commit()

    # Create Speakers
    speaker1 = Speaker(name="Alex Johnson")
    speaker2 = Speaker(name="Riley Chen")
    speaker3 = Speaker(name="Jordan Brooks")
    db.session.add_all([speaker1, speaker2, speaker3])
    db.session.commit()

    # Create Bios
    bio1 = Bio(bio_text="Expert in scalable backend systems with 10+ years of experience.", speaker=speaker1)
    bio2 = Bio(bio_text="AI researcher focusing on machine learning and data ethics.", speaker=speaker2)
    bio3 = Bio(bio_text="Software engineer passionate about teaching and open source.", speaker=speaker3)
    db.session.add_all([bio1, bio2, bio3])
    db.session.commit()

    # Associate Speakers and Sessions
    session1.speakers.append(speaker1)
    session2.speakers.append(speaker2)
    session2.speakers.append(speaker3)
    session3.speakers.append(speaker2)
    db.session.commit()

    print("🌱 Database seeded successfully!")
