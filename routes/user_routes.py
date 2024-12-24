# routes/user_routes.py

from flask import request, jsonify
from models import db, User

def get_user_profile():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "fullname": user.fullname,
            "email": user.email,
            "mob_no": user.mob_no
        }), 200
    return jsonify({"error": "User not found"}), 404

def update_user_profile():
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.json
    if 'fullname' in data:
        user.fullname = data['fullname']
    if 'mob_no' in data:
        user.mob_no = data['mob_no']
    
    db.session.commit()
    
    return jsonify({
        "message": "User profile updated successfully!",
        "user": {"fullname": user.fullname, "mob_no": user.mob_no}
    }), 200
