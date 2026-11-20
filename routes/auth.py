from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, AdminLoginForm # Assuming you’ve defined this form in forms.py
from routes.oauth_client import oauth
from models.user_utils import get_or_create_user
from models import User, Role
from app import db
import os  

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login/google')
def login_google():
    google = oauth.create_client('google')
    session['auth_flow'] = 'login'
    redirect_uri = url_for('auth.auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri, prompt='select_account')

@auth_bp.route('/register/google')
def register_google():
    google = oauth.create_client('google')
    role = request.args.get('role')
    if role not in ['student', 'instructor']:
        return "Invalid role", 400

    session['auth_flow'] = 'register'
    session['pending_role'] = role  # ✅ Store selected role
    redirect_uri = url_for('auth.auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri, prompt='select_account')

@auth_bp.route('/callback')
def auth_callback():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    user_info = token.get('userinfo') or google.parse_id_token(token)
    session['email'] = user_info['email']
    session['name'] = user_info['name']
    
    if session.get('auth_flow') == 'register':
        role = session.pop('pending_role', None)
        session['role'] = role
        user_info['role'] = role
        
        try:
            session['user_id'] = get_or_create_user(user_info)  
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('auth.register'))
    else:
        # Login flow
        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            flash("This email is not registered. Please sign up first.", "error")
            return redirect(url_for('auth.register'))

        session['user_id'] = user.user_id
        session['role'] = user.role.role_name
        session['name'] = user.name

    return redirect(url_for('dashboard.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    pass_ : str
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.username.data
        password = str(form.password.data)
        role_name = form.role.data

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'error')
            return redirect(url_for('auth.register'))
        role = Role.query.filter_by(role_name=role_name).first()
        hashed_pw = generate_password_hash(password)

        new_user = User(name=name, email=email, password=hashed_pw, role=role, status='active')
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    admin_form = AdminLoginForm()
    
    # Get current user info if already logged in
    current_user = None
    if 'user_id' in session:
        current_user = User.query.get(session['user_id'])

    if form.validate_on_submit():
        email = form.email.data
        password = str(form.password.data)

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('❌ Invalid Email ID.', 'email_error')
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password, password):
            flash('❌ Incorrect password.', 'password_error')
            return redirect(url_for('auth.login'))

        session['user_id'] = user.user_id  
        session['role'] = user.role.role_name
        session['name'] = user.name  # Add user's name to session
        
        flash(f'👋 Welcome back !', 'success')
        return redirect(url_for('dashboard.index'))  # centralized role router

    return render_template('login.html', form=form, admin_form=admin_form, current_user=current_user)

@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    admin_form = AdminLoginForm()
    form = LoginForm()  # Needed for rendering

    if admin_form.validate_on_submit():
        email = admin_form.email.data
        password = str(admin_form.password.data)

        user = User.query.filter_by(email=email).first()
        if not user or user.role.role_name != 'admin':
            flash('❌ Invalid admin credentials.', 'admin_error')
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password, password):
            flash('❌ Incorrect password.', 'admin_error')
            return redirect(url_for('auth.login'))

        session['user_id'] = user.user_id
        session['role'] = 'admin'
        session['name'] = user.name  # Add user's name to session
        flash(f'👋 Welcome back, {user.name}! (Admin)', 'success')
        return redirect(url_for('dashboard.admin_dashboard'))

    return render_template('login.html', form=form, admin_form=admin_form)


@auth_bp.route('/logout')
def logout():
    session.clear()
    # flash('👋 You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login', message='Logged out successfully.'))
