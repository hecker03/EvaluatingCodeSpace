from functools import wraps
from flask import session, redirect, url_for, flash
from utils.permission import has_permission

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'role' not in session or session['role'] != required_role:
                flash('Access denied. Insufficient permissions.')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return wrapped
    return decorator

def permission_required(permission_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            role = session.get('role')
            if not role or not has_permission(role, permission_name):
                flash('Access denied. Missing permission.')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return wrapped
    return decorator