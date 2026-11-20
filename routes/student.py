from pdb import run
from re import S
from flask import Blueprint, abort, render_template, request, redirect, url_for, session, flash, jsonify
from models import submission
from models import assignment
from utils.decorators import login_required, permission_required, role_required
import pandas as pd 
from gspread_dataframe import set_with_dataframe
from models.submission import CodeSubmission
from models.assignment import Assignment
from forms import SubmissionForm
from datetime import datetime
from sqlalchemy import true
from app import db
# from q import sheet
import requests
import gspread
import time

student_bp = Blueprint('student', __name__, url_prefix='/student')

# 🔐 RapidAPI Judge0 CE config
RAPIDAPI_KEY = "795d6776a7msh8fa04f060dbfd88p1053b5jsn20c745ecdbbd"
RAPIDAPI_HOST = "judge0-ce.p.rapidapi.com"
BASE_URL = f"https://{RAPIDAPI_HOST}/submissions"

HEADERS = {
    "Content-Type": "application/json",
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

LANGUAGE_MAP = {
    "python": 71,
    "cpp": 54,
    "java": 62
}

def calculate_grade(results):
    if not results or not isinstance(results, list):
        return 0, False

    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))
    score = int((passed / total) * 100) if total > 0.33 else 0
    return score, passed == total

def poll_until_ready(token, timeout=10):
    url = f"{BASE_URL}/{token}?base64_encoded=false&fields=compile_output,stderr,status,stdout,time"
    for _ in range(timeout):
        res = requests.get(url, headers=HEADERS).json()
        status_id = res.get("status", {}).get("id")
        if status_id in [3, 4, 5, 6, 7]:  # Final states
            return res
        time.sleep(1)
    return res

def run_test_cases(code, language, testcases):
    results = []
    language_id = LANGUAGE_MAP.get(language)
    if not testcases or not isinstance(testcases, list):
        return [{"error": "No valid testcases found"}]

    for case in testcases:
        if not all(k in case for k in ("input", "expected_output")):
            results.append({
                "input": case.get("input", ""),
                "expected": case.get("expected_output", ""),
                "actual": "",
                "status": "Invalid test case",
                "passed": False,
                "language_id": language_id
            })
            continue

        payload = {
            "source_code": code,
            "language_id": language_id,
            "stdin": case["input"]
        }

        try:
            res = requests.post(f"{BASE_URL}?base64_encoded=false&wait=false", json=payload, headers=HEADERS)
            token = res.json().get("token")
            sub_res = poll_until_ready(token)

            actual_output = sub_res.get("stdout", "").strip() if sub_res.get("stdout") else ""
            expected_output = case["expected_output"].strip()
            passed = actual_output == expected_output

            results.append({
                "input": case["input"],
                "expected": expected_output,
                "actual": actual_output,
                "status": sub_res.get("status", {}).get("description", "Unknown"),
                "passed": passed,
                "language_id": language_id
            })

        except Exception as e:
            results.append({
                "input": case["input"],
                "expected": case["expected_output"],
                "actual": "",
                "status": f"Error: {str(e)}",
                "passed": False,
                "language_id": language_id
            })

    return results

@student_bp.route('/submit/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
@role_required('student')
def submit_code(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    user_id = session.get('user_id')

    already_submitted = CodeSubmission.query.filter_by(
        user_id=user_id,
        assignment_id=assignment_id,
        status='submitted'
    ).first()

    if already_submitted:
        flash('✅ You have already submitted this assignment. Resubmission is not allowed.', 'info')
        return redirect(url_for('student.dashboard'))

    draft = CodeSubmission.query.filter_by(
        user_id=user_id,
        assignment_id=assignment_id,
        status='draft'
    ).first()

    form = SubmissionForm()

    if form.validate_on_submit():
        action = request.form.get('action')
        code = form.code.data
        language = form.language.data

        submission = draft if draft else CodeSubmission(user_id=user_id, assignment_id=assignment_id)
        submission.code = code
        submission.language = language
        submission.timestamp = datetime.utcnow()

        if action == 'save':
            submission.status = 'draft'
            flash('💾 Draft saved successfully.', 'info')
        elif action == 'submit':
            submission.status = 'submitted'
            testcases = getattr(assignment, 'testcases', None)
            results = run_test_cases(code, language, testcases)
            session['results'] = results
            score, all_passed = calculate_grade(results)
            submission.final_grade = score
            submission.auto_grade = all_passed
            flash(f'🚀 Submission successful.', 'success')

        db.session.add(submission)
        db.session.commit()
        return redirect(url_for('student.result'))

    if draft:
        form.code.data = draft.code
        form.language.data = draft.language

    return render_template("student/submit_code.html", assignment=assignment, draft=draft, form=form)

@student_bp.route('/submission/<int:id>')
@login_required
@role_required('student')
def view_submission(id):
    submission = CodeSubmission.query.get_or_404(id)
    assignment = Assignment.query.get(submission.assignment_id)

    if submission.user_id != session.get('user_id'):
        abort(403)

    return render_template('student/view_submission.html', submission=submission, assignment=assignment)

@student_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('student')
def edit_submission(id):
    submission = CodeSubmission.query.get_or_404(id)
    assignment = Assignment.query.get(submission.assignment_id)
    form = SubmissionForm(obj=submission)

    if form.validate_on_submit():
        submission.code = form.code.data
        submission.language = form.language.data
        submission.timestamp = datetime.utcnow()
        action = request.form.get('action')

        if action == 'save':
            flash('💾 Draft updated.', 'info')
        elif action == 'submit':
            submission.status = 'submitted'
            testcases = getattr(assignment, 'testcases', None)
            results = run_test_cases(submission.code, submission.language, testcases)
            session['results'] = results
            submission.final_grade = None
            flash('🚀 Submission successful.', 'success')

        db.session.commit()
        return redirect(url_for('student.result'))

    return render_template('student/submit_code.html', assignment=assignment, draft=submission, form=form)

@student_bp.route('/dashboard')
@login_required
@role_required('student')
def dashboard():
    user_id = session['user_id']

    submitted_ids = db.session.query(CodeSubmission.assignment_id)\
        .filter_by(user_id=user_id)\
        .filter(CodeSubmission.status != 'draft')\
        .distinct()

    pending_assignments = Assignment.query\
        .filter(~Assignment.assignment_id.in_(submitted_ids))\
        .order_by(Assignment.deadline.asc())\
        .all()

    submissions = CodeSubmission.query.filter_by(user_id=user_id)\
        .order_by(CodeSubmission.timestamp.desc()).all()

    return render_template('student/dashboard.html', assignments=pending_assignments, submissions=submissions)

@student_bp.route('/result')
@login_required
@role_required('student')
def result():
    results = session.get('results', [])
    score, all_passed = calculate_grade(results)
    webhook_url = "https://hook.eu2.make.com/qr1r702itc6fxlihexk4a634ecbfdphs"  # Replace with your actual webhook URL
    payload = {
        "user": session.get('user_id'),
        "language_id": results[0]["language_id"] if results else 71,
        "score": score,
        "passed": all_passed,
        "timestamp": datetime.utcnow().isoformat(),
        "results": results  # This is your full list of test case evaluations
    }

    response = requests.post(webhook_url, json=payload)
    print("Webhook sent:", response.status_code)

    return render_template('student/result.html', results=results)

@student_bp.route('/check_syntax', methods=['POST'])
def check_syntax():
    data = request.get_json(force=True)
    code = data.get('code')
    language = data.get('language')
    language_id = LANGUAGE_MAP.get(language)
    print("Checking syntax for language:", language_id)
    if not code or not language_id:
        return jsonify({"message": "Invalid code or language"}), 400

    payload = {
        "source_code": code,
        "language_id": language_id
    }

    try:
        url = f"{BASE_URL}?base64_encoded=false&wait=true&fields=compile_output,stderr,status"
        res = requests.post(url, json=payload, headers=HEADERS, timeout=20)

        # Guard against HTML responses
        if "application/json" not in res.headers.get("Content-Type", ""):
            return jsonify({
                "message": "Judge0 returned non-JSON",
                "status_code": res.status_code,
                "content_type": res.headers.get("Content-Type"),
                "body_snippet": res.text[:200]
            }), 502

        result = res.json()
        status = result.get("status", {}).get("description", "Unknown")
        status_id = result.get("status", {}).get("id", -1)

        return jsonify({
            "message": f"Syntax: {status}",
            "status_id": status_id,
            "compile_output": result.get("compile_output") or "",
            "stderr": result.get("stderr") or ""
        }), 200

    except Exception as e:
        return jsonify({"message": f"Error:"}), 500

