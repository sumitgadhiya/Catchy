import jwt
import datetime
from flask import current_app

def generate_token(user_id):
    """Generate a JWT token with a 1-hour expiration."""
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({"user_id": user_id, "exp": expiration}, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token

def decode_token(token):
    """Decode a JWT token to extract the payload."""
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
