from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SelectField, TextAreaField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, ValidationError
import json

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('student', 'Student'), ('instructor', 'Instructor')])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class AdminLoginForm(FlaskForm):
    email = StringField('Admin Email', validators=[DataRequired(), Email()])
    password = PasswordField('Admin Password', validators=[DataRequired()])

class AssignmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    input_format = TextAreaField('Input Format')
    output_format = TextAreaField('Output Format')
    constraints = TextAreaField('Constraints')
    sample_input = TextAreaField('Sample Input')
    sample_output = TextAreaField('Sample Output')
    deadline = DateTimeLocalField('Deadline', format='%Y-%m-%dT%H:%M')
    testcases_json = TextAreaField('Testcases (JSON)', validators=[DataRequired()])

    def validate_testcases_json(self, field):
        try:
            data = json.loads(field.data)
            if not isinstance(data, list):
                raise ValidationError("Testcases must be a JSON array.")
            for testcase in data:
                if not isinstance(testcase, dict) or "input" not in testcase or "expected_output" not in testcase:
                    raise ValidationError("Each testcase must have 'input' and 'expected_output' keys.")
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON format.")

class SubmissionForm(FlaskForm):
    code = TextAreaField('Code', validators=[DataRequired()])
    language = SelectField('Language', choices=[('python', 'Python'), ('cpp', 'C++'), ('java', 'Java')], validators=[DataRequired()])

class ReviewSubmissionForm(FlaskForm):
    final_grade = IntegerField('Final Grade (editable)', validators=[DataRequired()])
    feedback = TextAreaField('Instructor Feedback')
