# # routes/auth_routes.py

# from flask import request, jsonify
# from models import db, User

# def register():
#     data = request.json
#     if not all(key in data for key in ('fullname', 'email', 'mob_no', 'password', 'conf_pass')):
#         return jsonify({"error": "Missing fields"}), 400
    
#     if data['password'] != data['conf_pass']:
#         return jsonify({"error": "Passwords do not match"}), 400
    
#     existing_user = User.query.filter_by(email=data['email']).first()
#     if existing_user:
#         return jsonify({"error": "Email already exists"}), 409
    
#     new_user = User(
#         fullname=data['fullname'],
#         email=data['email'],
#         mob_no=data['mob_no'],
#         password=data['password'],
#         conf_pass=data['conf_pass']
#     )
    
#     db.session.add(new_user)
#     db.session.commit()
    
#     return jsonify({"message": "User registered successfully!", "user": data}), 201

# def login():
#     data = request.json
#     if not all(key in data for key in ('email', 'password')):
#         return jsonify({"error": "Missing email or password"}), 400

#     user = User.query.filter_by(email=data['email']).first()
#     if user and user.password == data['password']:
#         return jsonify({"message": "Login successful", "user": {"email": user.email, "fullname": user.fullname}}), 200
#     else:
#         return jsonify({"error": "Invalid email or password"}), 401






# import jwt
# import datetime
# from flask import request, jsonify
# from models import db, User
# from flask import current_app

# def generate_jwt(user_id, email, fullname):
#     # Create a JWT token
#     expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 1 hour expiry time
#     payload = {
#         'user_id': user_id,
#         'email': email,
#         'fullname': fullname,
#         'exp': expiration_time
#     }
#     token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
#     return token

# def register():
#     data = request.json
#     if not all(key in data for key in ('fullname', 'email', 'mob_no', 'password', 'conf_pass')):
#         return jsonify({"error": "Missing fields"}), 400
    
#     if data['password'] != data['conf_pass']:
#         return jsonify({"error": "Passwords do not match"}), 400
    
#     existing_user = User.query.filter_by(email=data['email']).first()
#     if existing_user:
#         return jsonify({"error": "Email already exists"}), 409
    
#     new_user = User(
#         fullname=data['fullname'],
#         email=data['email'],
#         mob_no=data['mob_no'],
#         password=data['password'],
#         conf_pass=data['conf_pass']
#     )
    
#     db.session.add(new_user)
#     db.session.commit()
    
#     return jsonify({"message": "User registered successfully!", "user": data}), 201

# def login():
#     data = request.json
#     if not all(key in data for key in ('email', 'password')):
#         return jsonify({"error": "Missing email or password"}), 400

#     user = User.query.filter_by(email=data['email']).first()
#     if user and user.password == data['password']:
#         # Generate JWT token upon successful login
#         token = generate_jwt(user.id, user.email, user.fullname)
#         return jsonify({
#             "message": "Login successful",
#             "user": {"email": user.email, "fullname": user.fullname},
#             "token": token
#         }), 200
#     else:
#         return jsonify({"error": "Invalid email or password"}), 401





# With OTP






import jwt
import datetime
import random
import smtplib
from email.mime.text import MIMEText
from flask import request, jsonify, session, current_app
from models import db, User

def generate_jwt(user_id, email, fullname):
    # Create a JWT token
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 1 hour expiry time
    payload = {
        'user_id': user_id,
        'email': email,
        'fullname': fullname,
        'exp': expiration_time
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def generate_otp():
    # Generate a random 6-digit OTP
    return str(random.randint(100000, 999999))

def send_otp_email(to_email, otp):
    # Email sending functionality using Gmail's SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = current_app.config['SMTP_EMAIL']
    sender_password = current_app.config['SMTP_PASSWORD']

    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}"
    
    # Create email message
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = to_email

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    return True

def register():
    data = request.json
    if not all(key in data for key in ('fullname', 'email', 'mob_no', 'password', 'conf_pass')):
        return jsonify({"error": "Missing fields"}), 400
    
    if data['password'] != data['conf_pass']:
        return jsonify({"error": "Passwords do not match"}), 400
    
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "Email already exists"}), 409
    
    # Generate OTP and expiry time
    otp = generate_otp()
    otp_expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)  # OTP expiry time (10 minutes)
    
    new_user = User(
        fullname=data['fullname'],
        email=data['email'],
        mob_no=data['mob_no'],
        password=data['password'],
        conf_pass=data['conf_pass'],
        otp=otp,
        otp_expiry=otp_expiry  # Save OTP expiry time
    )
    
    db.session.add(new_user)
    db.session.commit()

    # Send OTP via email
    email_sent = send_otp_email(data['email'], otp)
    if not email_sent:
        return jsonify({"error": "Registration successful, but failed to send OTP"}), 500
    
    # print(f"User registered. OTP: {otp}, Expiry: {otp_expiry}")
    return jsonify({
        "message": "User registered successfully! OTP sent to email.",
        "user": {"fullname": data['fullname'], "email": data['email']}
    }), 201



def verify_otp():
    data = request.json
    if not all(key in data for key in ('email', 'otp')):
        return jsonify({"error": "Email and OTP are required"}), 403

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"error": "User with this email does not exist"}), 404

    # Check if OTP exists and verify expiry time
    if not user.otp:
        return jsonify({"error": "No OTP generated for this user."}), 402

    if datetime.datetime.utcnow() > user.otp_expiry:
        # OTP has expired
        return jsonify({"error": "OTP has expired. Please request a new one."}), 401


    # print(f"User registered. OTP: {user.otp}")
    # print(f"User side registered. OTP: {data['otp']}")
    # Verify OTP
    # if user.otp == data['otp']:
    if str(user.otp).strip() == str(data['otp']).strip():
        # OTP verified successfully, clear OTP from the database
        print(f"User registered. OTP: {user.otp}, Expiry: {user.otp_expiry}")

        user.otp = None
        user.otp_expiry = None
        db.session.commit()

        return jsonify({
            "message": "OTP verified successfully",
            "user": {"email": user.email, "fullname": user.fullname}
        }), 200
    else:
        return jsonify({"error": "Invalid OTP"}), 400





def login():
    data = request.json
    if not all(key in data for key in ('email', 'password')):
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == data['password']:
        # Generate JWT token upon successful login
        token = generate_jwt(user.id, user.email, user.fullname)
        return jsonify({
            "message": "Login successful",
            "user": {"email": user.email, "fullname": user.fullname},
            "token": token
        }), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401






def check_email():
    data = request.json

    if 'email' not in data:
        return jsonify({"error": "Email is required"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"error": "User with this email does not exist"}), 404

    return jsonify({
        "message": "Email exists, you can proceed to reset your password",
        "email": user.email
    }),200




def forgot_password():
    data = request.json

    if not all(key in data for key in ('email', 'new_password', 'conf_pass')):
        return jsonify({"error": "Email and new password are required"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"error": "User with this email does not exist"}), 404

    # Update the user's password (ensure it's hashed for security)
    from werkzeug.security import generate_password_hash
    user.password = (data['new_password'])
    user.conf_pass = (data['conf_pass'])

    db.session.commit()

    return jsonify({"message": "Password has been reset successfully"}), 200