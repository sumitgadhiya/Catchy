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






import jwt
import datetime
from flask import request, jsonify
from models import db, User
from flask import current_app

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

def register():
    data = request.json
    if not all(key in data for key in ('fullname', 'email', 'mob_no', 'password', 'conf_pass')):
        return jsonify({"error": "Missing fields"}), 400
    
    if data['password'] != data['conf_pass']:
        return jsonify({"error": "Passwords do not match"}), 400
    
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "Email already exists"}), 409
    
    new_user = User(
        fullname=data['fullname'],
        email=data['email'],
        mob_no=data['mob_no'],
        password=data['password'],
        conf_pass=data['conf_pass']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully!", "user": data}), 201

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



