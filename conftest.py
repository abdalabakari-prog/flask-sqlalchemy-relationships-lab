import pytest
import sys
import os
from pathlib import Path

# Add server directory to path if it exists
server_path = Path(__file__).parent / "server"
if server_path.exists():
    sys.path.insert(0, str(server_path))

# Try importing from server module first, then fallback to direct import
try:
    from server.app import app, db
    from server.models import Event, Session, Speaker, Bio
except ImportError:
    try:
        from app import app, db
        from models import Event, Session, Speaker, Bio
    except ImportError:
        # Last resort - add current directory
        sys.path.insert(0, str(Path(__file__).parent))
        from app import app, db
        from models import Event, Session, Speaker, Bio

import datetime

@pytest.fixture(scope="function")
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()

        event = Event(name="Tech Conference", location="New York")
        db.session.add(event)
        db.session.commit()

        session = Session(
            title="Future of AI",
            start_time=datetime.datetime(2024, 6, 1, 9, 0),
            event=event
        )
        db.session.add(session)

        speaker = Speaker(name="Jane Doe")
        db.session.add(speaker)

        bio = Bio(bio_text="Expert in AI and ML.", speaker=speaker)
        db.session.add(bio)

        session.speakers.append(speaker)

        db.session.commit()

        yield app.test_client()

        db.session.remove()
        db.drop_all()
