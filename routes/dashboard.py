from flask import Blueprint, session, redirect, url_for, request, render_template, flash
from models import user
from models.assignment import Assignment
from models.submission import CodeSubmission
from utils.decorators import login_required, role_required
from app import db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
def index():
    role = session.get('role')

    if not role:
        return redirect(url_for('auth.login', error='Please log in first.'))

    if role == 'student':
        return redirect(url_for('dashboard.student_dashboard'))
    elif role == 'instructor':
        return redirect(url_for('dashboard.instructor_dashboard'))
    elif role == 'admin':
        return redirect(url_for('dashboard.admin_dashboard'))
    else:
        return redirect(url_for('auth.login', error='Unknown role.'))

@dashboard_bp.route('/student')
@login_required
@role_required('student')
def student_dashboard():
    user_id = session.get('user_id')

    # Get assignment IDs already submitted (excluding drafts)
    submitted_ids = db.session.query(CodeSubmission.assignment_id)\
        .filter_by(user_id=user_id)\
        .filter(CodeSubmission.status != 'draft')\
        .distinct()

    # Filter assignments that have NOT been submitted yet
    assignments = Assignment.query\
        .filter(~Assignment.assignment_id.in_(submitted_ids))\
        .order_by(Assignment.deadline.asc())\
        .all()

    # You can still show all submissions if needed
    submissions = CodeSubmission.query.filter_by(user_id=user_id).all()
    return render_template('student/dashboard.html', assignments=assignments, submissions=submissions)


@dashboard_bp.route('/instructor')
@login_required
@role_required('instructor')
def instructor_dashboard():
    instructor_id = session.get('user_id')
    if session.get('role') != 'instructor':
        flash('Access denied: Instructors only.', 'danger')
        return redirect(url_for('dashboard.index'))

    # Get assignments created by this instructor
    assignments = Assignment.query.filter_by(created_by=instructor_id).all()

    # Get submissions for those assignments
    assignment_ids = [a.assignment_id for a in assignments]
    submissions = CodeSubmission.query.filter(CodeSubmission.assignment_id.in_(assignment_ids)).all()
    
    return render_template('instructor/dashboard.html', assignments=assignments, submissions=submissions)

@dashboard_bp.route('/admin')
@login_required
@role_required('admin')
def admin_dashboard():
    return render_template('admin/dashboard.html')