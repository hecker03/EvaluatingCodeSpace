from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import User, Role
from extensions import db  # assuming you've modularized db
from utils.decorators import login_required, role_required
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/audit')
@login_required
@role_required('admin')
def view_logs():
    users = User.query.order_by(User.user_id.desc()).all()
    return render_template('admin/view_logs.html', users=users)

@admin_bp.route('/assign-role', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def assign_role():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        role_id = request.form.get('role_id')

        user = User.query.get(user_id)
        if user:
            user.role_id = role_id
            db.session.commit()

            # Optional: flash message or audit log
            flash(f"Role updated successfully for {user.email}")
            return redirect(url_for('admin.assign_role'))
        else:
            flash("User not found.")
            return redirect(url_for('admin.assign_role'))

    users = User.query.all()
    roles = Role.query.all()
    return render_template('admin/assign_role.html', users=users, roles=roles)