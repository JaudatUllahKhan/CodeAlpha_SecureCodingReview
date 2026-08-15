import sqlite3
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded Secret Key
app.config['SECRET_KEY'] = 'super-secret-hardcoded-key-12345'

def get_db():
    conn = sqlite3.connect('app.db')
    return conn

@app.route('/')
def home():
    return '''
    <h2>Vulnerable Web Application Audit Target</h2>
    <ul>
        <li><a href="/login?username=admin">Login Test (SQLi)</a></li>
        <li><a href="/ping?host=127.0.0.1">Ping Tool (Command Injection)</a></li>
        <li><a href="/profile?name=Visitor">Profile (Reflected XSS)</a></li>
    </ul>
    '''

# VULNERABILITY 2: SQL Injection (SQLi)
@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    
    conn = get_db()
    cursor = conn.cursor()
    # INSECURE: Direct string concatenation into SQL query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"[LOG] Executing Query: {query}")
    
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            return f"Welcome back, {user[1]}!"
        return "Invalid credentials."
    except Exception as e:
        return f"Database Error: {str(e)}"

# VULNERABILITY 3: Command Injection
@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host', '127.0.0.1')
    # INSECURE: Passing untrusted user input directly into system shell command
    command = f"ping -n 1 {host}" if subprocess.os.name == 'nt' else f"ping -c 1 {host}"
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return f"<pre>{output}</pre>"
    except Exception as e:
        return f"Execution Error: {str(e)}"

# VULNERABILITY 4: Reflected Cross-Site Scripting (XSS)
@app.route('/profile', methods=['GET'])
def profile():
    name = request.args.get('name', 'Guest')
    # INSECURE: Unescaped raw string formatting directly into HTML response
    template = f"<h1>User Profile: {name}</h1><p>Welcome to your portal.</p>"
    return render_template_string(template)

if __name__ == '__main__':
    app.run(debug=True, port=5000)