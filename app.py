from flask import Config, Flask, render_template
from extensions import db
from dotenv import load_dotenv
from config import Config
from flask_wtf import CSRFProtect
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.student import student_bp
from routes.instructor import instructor_bp
from routes.chat import chat_bp
import os
from routes.oauth_client import oauth

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)
db.init_app(app)
oauth.init_app(app)

oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Register blueprints
app.register_blueprint(dashboard_bp)
app.register_blueprint(student_bp)
app.register_blueprint(instructor_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)

@app.after_request
def disable_client_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, threaded=True)