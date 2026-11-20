from app import db

class Permission(db.Model):
    __tablename__ = 'permissions'
    permission_id = db.Column(db.Integer, primary_key=True)
    action_name = db.Column(db.String(50), unique=True, nullable=False)
    resource = db.Column(db.String(50))
    description = db.Column(db.Text)