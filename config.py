# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@localhost:3306/catchy_db'  # Update if needed
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SMTP_EMAIL = os.getenv('sp5562264@gmail.com')  # Your email address
    SMTP_PASSWORD = os.getenv('ynhv lvch hrlv nebv')  # Your email password


