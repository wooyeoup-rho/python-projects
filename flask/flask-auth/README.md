# Flask Authentication

Simple **Flask** website demonstrating basic authentication with **Flask-Login** and **Werkzeug** for hashing.

## Showcase

https://github.com/user-attachments/assets/a71150a9-7c71-4010-8a65-bd2a4479eae9

## How It Works
1. Flask-Login handles tracking whether a user is logged in during a session and protects certain routes so that they're only accesible for a logged in user.
2. During User object creation, Werkzeug is used to generate a password hash using PBKDF2 with SHA-256.

## Technologies Used
- Python
- Flask
- Flask-Login
- Werkzeug
