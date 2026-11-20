from flask import Blueprint, abort, render_template, request, redirect, url_for, session, flash
from utils.decorators import login_required, permission_required, role_required
from forms import AssignmentForm, ReviewSubmissionForm
from models.submission import CodeSubmission
from models.assignment import Assignment
from models.user import User
from datetime import datetime
from app import db
import json

instructor_bp = Blueprint('instructor', __name__, url_prefix='/instructor', template_folder='templates')

@instructor_bp.route('/submissions')
@login_required
@role_required('instructor')
def submissions_list():
    user_id = session['user_id']

    submissions = CodeSubmission.query\
        .order_by(CodeSubmission.timestamp.desc())\
        .all()

    assignments = Assignment.query.filter_by(created_by=user_id)\
        .order_by(Assignment.deadline.asc()).all()

    return render_template('instructor/dashboard.html', submissions=submissions, assignments=assignments)

@instructor_bp.route('/review/<int:submission_id>', methods=['GET', 'POST'])
@login_required
@role_required('instructor')
@permission_required('review_submission')
def review_submission(submission_id):
    submission = CodeSubmission.query.get_or_404(submission_id)
    assignment = Assignment.query.get(submission.assignment_id)

    if assignment.created_by != session.get('user_id'):
        abort(403)

    form = ReviewSubmissionForm()

    if form.validate_on_submit():
        submission.final_grade = form.final_grade.data
        submission.feedback = form.feedback.data
        db.session.commit()
        flash('✅ Grade and feedback saved successfully.', 'success')
        return redirect(url_for('instructor.submissions_list'))

    form.final_grade.data = submission.final_grade or submission.auto_grade
    form.feedback.data = submission.feedback

    return render_template('instructor/review_submission.html', submission=submission, form=form)

@instructor_bp.route('/create_assignment', methods=['GET', 'POST'])
@login_required
@role_required('instructor')
@permission_required('upload_assignment')
def create_assignment():
    form = AssignmentForm()
    if form.validate_on_submit():
        assignment = Assignment(
            title=form.title.data,
            description=form.description.data,
            input_format=form.input_format.data,
            output_format=form.output_format.data,
            constraints=form.constraints.data,
            sample_input=form.sample_input.data,
            sample_output=form.sample_output.data,
            deadline=form.deadline.data,
            created_by=session['user_id']
        )
        try:
            if form.testcases_json.data:
                parsed = json.loads(form.testcases_json.data)
                if isinstance(parsed, list):
                    assignment.testcases = parsed
        except Exception:
            flash('⚠️ Could not parse testcases JSON. Skipping.', 'warning')

        db.session.add(assignment)
        db.session.commit()
        flash('✅ Assignment created successfully.', 'success')
        return redirect(url_for('instructor.submissions_list'))

    return render_template('instructor/create_assignment.html', form=form)

@instructor_bp.route('/edit-assignment/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('instructor')
def edit_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    form = AssignmentForm(obj=assignment)

    if request.method == 'GET':
        try:
            form.testcases_json.data = json.dumps(assignment.testcases or [], ensure_ascii=False, indent=2)
        except Exception:
            form.testcases_json.data = ''

    if form.validate_on_submit():
        form.populate_obj(assignment)
        try:
            if form.testcases_json.data:
                parsed = json.loads(form.testcases_json.data)
                if isinstance(parsed, list):
                    assignment.testcases = parsed
        except Exception:
            flash('⚠️ Could not parse testcases JSON. Skipping.', 'warning')

        db.session.commit()
        flash('✅ Assignment updated successfully.', 'success')
        return redirect(url_for('instructor.submissions_list'))

    return render_template('instructor/edit_assignment.html', form=form, assignment=assignment)
