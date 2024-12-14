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
from routes.auth_routes import register, login
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

CORS(app)

# Configure app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/catchy_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback_secret_key_here")  # Get SECRET_KEY from .env or fallback

# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()

# Enable CORS
CORS(app)

# Define routes
app.add_url_rule('/register', 'register', register, methods=['POST'])
app.add_url_rule('/login', 'login', login, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
