# CodeAlpha Cyber Security Internship - Task 3: Secure Coding Review

A comprehensive secure code review and Static Application Security Testing (SAST) audit performed on a Python Flask web application. This project was completed as part of **Task 3** for the **CodeAlpha Cyber Security Internship**.

---

## 📌 Project Overview

This repository demonstrates the process of auditing a vulnerable Python Flask application, identifying security risks using static analysis, and implementing secure coding remediations to resolve all high- and medium-severity vulnerabilities.

* **Target Language**: Python 3.11+
* **Framework**: Flask
* **SAST Tooling**: Bandit (Python Security Static Analyzer)
* **Repository**: [CodeAlpha_SecureCodingReview](https://github.com/JaudatUllahKhan/CodeAlpha_SecureCodingReview)

---

## 🔍 Vulnerability Audit & Remediation Matrix

| Vulnerability Type | Initial Severity | Vulnerable Code Pattern (`vulnerable_app.py`) | Remediation Applied (`secure_app.py`) | Final Status |
| :--- | :--- | :--- | :--- | :--- |
| **Command Injection** (`B602`) | 🔴 High | `subprocess.check_output(command, shell=True)` | Removed `shell=True`, implemented argument array execution, and added regex pattern input validation. | ✅ Resolved |
| **Werkzeug Debug Exposure** (`B201`) | 🔴 High | `app.run(debug=True)` | Disabled debug mode in application configuration (`debug=False`). | ✅ Resolved |
| **SQL Injection (SQLi)** (`B608`) | 🟡 Medium | Dynamic string formatting: `f"SELECT ... '{username}'"` | Implemented parameterized SQL queries using SQLite `?` placeholders. | ✅ Resolved |
| **Hardcoded Secrets** (`B105`) | 🟢 Low | Static configuration key: `app.config['SECRET_KEY'] = '...'` | Loaded secret keys dynamically from environment variables (`os.getenv`). | ✅ Resolved |
| **Reflected XSS** | 🟡 Medium | Unescaped parameter formatting directly into HTML templates | Implemented HTML entity sanitization (`html.escape`). | ✅ Resolved |

---

## 🛠️ Static Application Security Testing (SAST)

Static code analysis was executed using **Bandit**.

### 1. Install Dependencies
```bash
pip install flask bandit