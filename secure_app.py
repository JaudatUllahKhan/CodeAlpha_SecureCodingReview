import os
import sqlite3
import subprocess
import html
from flask import Flask, request, render_template

app = Flask(__name__)

# FIX 1: Fetch secret key from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))

def get_db():
    conn = sqlite3.connect('app.db')
    return conn

@app.route('/')
def home():
    return '''
    <h2>Secured Web Application Portal</h2>
    <ul>
        <li><a href="/login?username=admin">Login Test (Parameterized)</a></li>
        <li><a href="/ping?host=127.0.0.1">Ping Tool (Input Validated)</a></li>
        <li><a href="/profile?name=Visitor">Profile (HTML Sanitized)</a></li>
    </ul>
    '''

# FIX 2: Parameterized Queries (Prevents SQL Injection)
@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    
    conn = get_db()
    cursor = conn.cursor()
    # SECURE: Using placeholder parameters (?)
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    
    try:
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        if user:
            return f"Welcome back, {html.escape(user[1])}!"
        return "Invalid credentials."
    except Exception as e:
        return "An error occurred during authentication."

# FIX 3: Argument Lists & Input Validation (Prevents Command Injection)
@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host', '127.0.0.1')
    
    # Validate host IP address format basic check
    import re
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        return "Invalid host input detected.", 400
        
    param = '-n' if subprocess.os.name == 'nt' else '-c'
    # SECURE: Pass array without shell=True to avoid subshell execution
    try:
        output = subprocess.check_output(['ping', param, '1', host], text=True, stderr=subprocess.STDOUT)
        return f"<pre>{html.escape(output)}</pre>"
    except Exception as e:
        return "Failed to execute ping operation."

# FIX 4: Output Encoding / Contextual Escaping (Prevents Reflected XSS)
@app.route('/profile', methods=['GET'])
def profile():
    name = request.args.get('name', 'Guest')
    # SECURE: Explicit HTML sanitization on untrusted input
    safe_name = html.escape(name)
    return f"<h1>User Profile: {safe_name}</h1><p>Welcome to your portal.</p>"

if __name__ == '__main__':
    # Disable debug mode in production context
    app.run(debug=False, port=5000)