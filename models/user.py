from app import db
from extensions import db
class User(db.Model):
    def __init__(self, name, email, password, role, status):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.status = status

    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255)) 
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    role = db.Column(db.String(50))
    institution = db.Column(db.String(100))
    registration_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(20), default='active')

    role = db.relationship('Role', backref='users')