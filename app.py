# from flask import Flask
# from flask_cors import CORS
# from config import Config
# from models import db
# import routes

# app = Flask(__name__)

# # Enable CORS for specific origins
# CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://localhost:5174"]}})

# app.config.from_object(Config)

# # Initialize the database with the app
# db.init_app(app)

# # Create tables if they don't exist
# with app.app_context():
#     db.create_all()

# # Register routes
# app.add_url_rule('/register', 'register', routes.register, methods=['POST'])
# app.add_url_rule('/login', 'login', routes.login, methods=['POST'])
# app.add_url_rule('/user/profile', 'get_user_profile', routes.get_user_profile, methods=['GET'])
# app.add_url_rule('/user/update', 'update_user_profile', routes.update_user_profile, methods=['PUT'])

# if __name__ == '__main__':
#     app.run(debug=True)








from flask import Flask
from flask_cors import CORS
from models import db
from routes.auth_routes import register, login, verify_otp, forgot_password, check_email
from routes.broker import broker, get_broker

import os
from dotenv import load_dotenv

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json


from flask_mail import Mail, Message
from flask_session import Session



# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

app.config.from_object('config.Config')

# CORS(app)
# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

migrate = Migrate(app, db)



mail = Mail(app)



# Configure app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/catchy_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback_secret_key_here")  # Get SECRET_KEY from .env or fallback
app.config['SMTP_EMAIL'] = 'sp5562264@gmail.com'
app.config['SMTP_PASSWORD'] = 'ynhv lvch hrlv nebv'
app.config['SESSION_TYPE'] = 'filesystem'


Session(app)


# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()

# Enable CORS
# CORS(app)

# Define routes
app.add_url_rule('/register', 'register', register, methods=['POST'])
app.add_url_rule('/login', 'login', login, methods=['POST'])
app.add_url_rule('/broker', 'broker', broker, methods=['POST'])
app.add_url_rule('/get_broker', 'get_broker', get_broker, methods=['GET'])  
app.add_url_rule('/verify_otp', 'verify_otp', verify_otp, methods=['POST'])
app.add_url_rule('/forgot_password', 'forgot_password', forgot_password, methods=['POST'])  
app.add_url_rule('/check_email', 'check_email', check_email, methods=['POST'])  






# if __name__ == '__main__':
#     app.run(debug=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)





