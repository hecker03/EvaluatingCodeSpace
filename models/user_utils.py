import email
from models import User
from app import db
from models.role import Role

def get_or_create_user(user_info):
    email = user_info['email']
    name = user_info.get('name', '')
    role_name = user_info.get('role')

    user = User.query.filter_by(email=email).first()
    if user:
        # ✅ Prevent role mismatch
        if user.role and user.role.role_name != role_name:
            raise ValueError(
                f"Email {email} already registered as {user.role.role_name}, cannot register as {role_name}."
            )
        return user.user_id

    role_obj = Role.query.filter_by(role_name=role_name).first()
    if not role_obj:
        raise ValueError(f"Role '{role_name}' not found in DB")

    user = User(
        email=email,
        name=name,
        role=role_obj,
        password='google_oauth',
        status='active'
    )
    db.session.add(user)
    db.session.commit()
    return user.user_id