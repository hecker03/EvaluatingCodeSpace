# 🚀 EvaluatingCodeSpace

> **The Next-Gen Automated Code Evaluation Platform with AI Assistance**

EvaluatingCodeSpace is a robust, secure, and intelligent platform designed to streamline the coding education process. It empowers instructors to create assignments with automated test cases and provides students with a secure sandbox to practice and submit their code, now enhanced with a **GenAI-powered Chatbot** for real-time assistance.

---

## ✨ Key Features

### 🤖 **AI-Powered Assistance**
- **Integrated GenAI Chatbot**: Powered by **Google Gemini 2.0 Flash**, our intelligent assistant is available on every page to help students clarify concepts and debug logic without giving away answers.
- **Floating Widget**: Accessible, non-intrusive UI for seamless interaction.

### 🔐 **Secure & Robust Architecture**
- **OAuth 2.0 Authentication**: Secure login via Google Accounts ensures verified identity management.
- **Role-Based Access Control (RBAC)**: Distinct portals and permissions for **Students**, **Instructors**, and **Admins**.
- **CSRF Protection**: Full protection against Cross-Site Request Forgery attacks.

### ⚡ **Automated Evaluation Engine**
- **Instant Feedback**: Student submissions are automatically run against defined test cases.
- **Dockerized Sandbox**: Code execution happens inside isolated **Docker containers** (Alpine Linux), ensuring security by restricting network access and resource usage.
- **Support for Python**: Optimized for Python 3.11 submissions.

### 📝 **Assignment Management**
- **Instructor Dashboard**: Create assignments, set deadlines, and define hidden/public test cases.
- **Student Dashboard**: View pending assignments, track submission history, and see real-time results.

---

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Database**: MySQL (SQLAlchemy ORM)
- **AI Engine**: Google Gemini API
- **Security**: Docker, OAuthlib, Flask-WTF
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

---

## 🚀 Getting Started

Follow these steps to set up the project locally.

### Prerequisites
- Python 3.8+
- MySQL Server
- Docker Desktop (running)
- Google Cloud Console Project (for OAuth & Gemini API)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/EvaluatingCodeSpace.git
    cd EvaluatingCodeSpace
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**
    Create a `.env` file in the root directory:
    ```env
    # Database
    DATABASE_URL="mysql+pymysql://user:password@localhost/ecs_platform"
    
    # Security
    SECRET_KEY="your_secret_key"
    
    # Google OAuth
    GOOGLE_CLIENT_ID="your_google_client_id"
    GOOGLE_CLIENT_SECRET="your_google_client_secret"
    
    # AI Chatbot
    GOOGLE_API_KEY="your_gemini_api_key"
    
    # Feature Flags
    ENABLE_AUTO_EVAL=true
    ENABLE_DOCKER_SANDBOX=true
    ```

5.  **Initialize Database**
    ```bash
    flask db upgrade
    # OR manually import db.sql if provided
    ```

6.  **Run the Application**
    ```bash
    python ./run_dev.py
    ```
    Visit `http://localhost:5000` in your browser.

---

## 🧪 Test Case Format

When creating assignments, test cases should be provided in JSON format:

```json
[
  {
    "input": "5\n",
    "output": "120\n"
  },
  {
    "input": "3\n",
    "output": "6\n"
  }
]
```

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

<p align="center">
  © 2025 EvaluatingCodeSpace. Built with ❤️ for Education.
</p>
