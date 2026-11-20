from xmlrpc.client import DateTime
from app import db

class CodeSubmission(db.Model):
    __tablename__ = 'code_submission'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.assignment_id'))

    code = db.Column(db.Text)  # Raw code
    language = db.Column(db.String(20))  # 'python', 'cpp', etc.
    status = db.Column(db.String(20))  # 'draft', 'submitted', 'graded'

    auto_grade = db.Column(db.Float)  # Result from sandbox evaluation
    final_grade = db.Column(db.Float)  # Instructor override
    feedback = db.Column(db.Text)  # Instructor comments

    sandbox_id = db.Column(db.String(100))  # Optional: ID from sandbox engine
    version = db.Column(db.Integer, default=1)  # For resubmissions
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref='submissions')
    assignment = db.relationship('Assignment', backref='submissions')