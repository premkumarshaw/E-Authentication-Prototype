from flask import Flask, request, jsonify, session, redirect, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
import random, string, qrcode
from io import BytesIO
import base64
import smtplib
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'Prem##Secure_Auth##'
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'my@SQL2025placement'
app.config['MYSQL_DB'] = 'e_auth_db'
app.config['MSQL_PORT'] = 3306

mysql = MySQL(app)

qr_sessions = {}

@app.route('/')
def root_redirect():
    return redirect('/pc_login')

@app.route('/pc_login')
def pc_login():
    return render_template('pc_login.html')

@app.route('/mobile_login')
def mobile_login():
    return render_template('mobile_login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/mobile_dashboard')
def mobile_dashboard():
    return render_template('dashboard_mobile.html')


@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s OR email=%s", (username, email))
    if cur.fetchone():
        return jsonify({'status': 'user exists'})

    cur.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s)", (username, email, password))
    mysql.connection.commit()
    return jsonify({'status': 'registered'})

@app.route('/api/send_otp', methods=['POST'])
def send_otp():
    data = request.json
    otp = ''.join(random.choices(string.digits, k=6))
    session['otp'] = otp
    session['otp_user'] = data['username']

    cur = mysql.connection.cursor()
    cur.execute("SELECT email FROM users WHERE username=%s OR email=%s", (data['username'], data['username']))
    result = cur.fetchone()
    if not result:
        return jsonify({'status': 'user not found'})
    
    receiver_email = result[0]
    send_email_otp(receiver_email, otp)
    return jsonify({'status': 'otp_sent'})

@app.route('/api/verify_otp', methods=['POST'])
def verify_otp():
    data = request.json
    if data['otp'] == session.get('otp') and data['username'] == session.get('otp_user'):
        session['user'] = data['username']
        return jsonify({'status': 'verified'})
    return jsonify({'status': 'invalid'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    login_input = data['username']
    password = data['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT password FROM users WHERE username=%s OR email=%s", (login_input, login_input))
    result = cur.fetchone()

    if result and check_password_hash(result[0], password):
        session['otp_user'] = login_input
        return jsonify({'status': 'otp_sent'})

    return jsonify({'status': 'failed'})

@app.route('/api/create_session', methods=['POST'])
def create_session():
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    qr_sessions[token] = {'verified': False, 'username': None}
    img = qrcode.make(token)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_url = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("utf-8")
    return jsonify({'token': token, 'qr_url': qr_url})

@app.route('/api/verify_qr', methods=['POST'])
def verify_qr():
    data = request.json
    token = data.get('token')
    user_id = data.get('user_id')
    if token in qr_sessions:
        qr_sessions[token]['verified'] = True
        qr_sessions[token]['username'] = user_id
        return jsonify({'status': 'verified'})
    return jsonify({'status': 'invalid token'})

@app.route('/api/check_session')
def check_session():
    token = request.args.get('token')
    if token in qr_sessions and qr_sessions[token]['verified']:
        session['user'] = qr_sessions[token]['username']
        return jsonify({'status': 'verified', 'redirect': '/dashboard'})
    return jsonify({'status': 'pending'})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'status': 'logged out'})

@app.route('/api/current_user')
def current_user():
    username = session.get('user')
    return jsonify({'username': username}) if username else jsonify({'username': None})

def send_email_otp(receiver_email, otp):
    smtp_server = "smtp.titan.email"
    smtp_port = 465 
    smtp_username = "noreply@locknlogin.tech"
    smtp_password = "Project7@2025"

    msg = EmailMessage()
    msg['Subject'] = "Your OTP Code"
    msg['From'] = smtp_username
    msg['To'] = receiver_email
    msg.set_content(f"Your OTP is: {otp}")

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
            smtp.login(smtp_username, smtp_password)
            smtp.send_message(msg)
            print("OTP sent successfully")
    except Exception as e:
        print("Error sending email:", e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
