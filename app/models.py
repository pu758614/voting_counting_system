from datetime import datetime
import pytz
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Define the Taipei timezone
taipei_tz = pytz.timezone('Asia/Taipei')

def taipei_time():
    """Return current time in Taipei timezone"""
    return datetime.now(taipei_tz)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    total_voters = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=taipei_time)
    threshold_type = db.Column(db.String(50), nullable=False)  # 'percentage' or 'majority'
    threshold_value = db.Column(db.Float, nullable=False)  # If 'percentage', this is the percentage value (e.g., 0.5 for 50%)
    candidates = db.relationship('Candidate', backref='election', lazy=True, cascade="all, delete-orphan")
    is_completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Election {self.title}>'

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    votes = db.Column(db.Integer, default=0)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    is_elected = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Candidate {self.name}>'

class VoteLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    vote_type = db.Column(db.String(1), nullable=False)  # '+' or '-'
    timestamp = db.Column(db.DateTime, default=taipei_time)

    candidate = db.relationship('Candidate', backref='vote_logs')
    election = db.relationship('Election', backref='vote_logs')

    def __repr__(self):
        return f'<VoteLog {self.candidate.name} {self.vote_type}>'