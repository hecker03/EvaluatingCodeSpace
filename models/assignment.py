from datetime import datetime
from extensions import db
from app import db
from sqlalchemy.dialects.mysql import JSON

class Assignment(db.Model):
    __tablename__ = 'assignments'

    assignment_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    input_format = db.Column(db.Text)
    output_format = db.Column(db.Text)
    constraints = db.Column(db.Text)
    sample_input = db.Column(db.Text)
    sample_output = db.Column(db.Text)

    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    deadline = db.Column(db.DateTime)
    # JSON list of {"input": str, "output": str}
    testcases = db.Column(JSON, default=list)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', backref='assignments')