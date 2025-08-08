# Two-Factor Authentication Web App

## 🔒 Project Overview

A cross-device 2FA system allowing users to register/login via OTP (email-based) and securely log in on PC using QR code scanned from their logged-in mobile session.

## 🚀 Features

* User Registration (email & password)
* Email-based OTP verification (via Gmail SMTP)
* Login via mobile or PC
* QR-based second-factor authentication
* Role-specific dashboards (PC and Mobile)
* Secure sessions with Flask sessions
* MySQL database integration

---

## 📦 Tech Stack

| Layer         | Technology                |
| ------------- | ------------------------- |
| Frontend      | HTML, CSS, JS             |
| Backend       | Python (Flask)            |
| Database      | MySQL                     |
| QR Generation | `qrcode` Python lib       |
| OTP Sending   | Gmail SMTP (App Password) |

---

## 🛠️ Prerequisites

### 1. Software

* Python 3.7+
* MySQL Server
* Ngrok (for mobile QR scan support)

### 2. Python Packages

Install with pip:

```bash
pip install flask flask-mysqldb flask-cors qrcode
```

### 3. MySQL Setup

```sql
CREATE DATABASE e_auth_db;

USE e_auth_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);
```

### 4. Gmail SMTP Setup

* Enable 2-Step Verification: [https://myaccount.google.com/security](https://myaccount.google.com/security)
* Generate App Password:

  * Select "Mail"
  * Select your device (e.g., "Windows Computer")
  * Click "Generate"
* Copy the 16-digit password and use it in `app.py` as:

```python
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
```

---

## 🏁 Running the App

### 1. Start Flask App

```bash
python app.py
```

### 2. Run Ngrok (for QR scan on mobile)

```bash
ngrok http 5000
```

Use the HTTPS URL provided by Ngrok (e.g., `https://abcd1234.ngrok.io`) on your mobile.

---

## 📁 Folder Structure

```
project/
│
├── app.py
├── templates/
│   ├── pc_login.html
│   ├── mobile_login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── dashboard_mobile.html
│   └── scan.html
```

---

## 👥 Team Handoff Instructions

* Ensure Python and MySQL are properly installed
* Share `.env` or Gmail app password securely (DO NOT commit it)
* Test locally on both PC and mobile
* Use Ngrok for testing secure camera access

---

## 🛡️ Security Notes

* All passwords should be hashed before storage (implement next)
* Use HTTPS in production
* Sanitize and validate all user inputs

---

## 📧 Contact

For issues, contact: `your_email@gmail.com`
