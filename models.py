# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mob_no = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    conf_pass = db.Column(db.String(100), nullable=False)
    otp = db.Column(String(6), nullable=True)  # OTP field
    otp_expiry = db.Column(DateTime, nullable=True)  # Expiry time for OTP


    def __repr__(self):
        return f'<User {self.fullname}>'




class Broker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    broker_name = db.Column(db.String(100), nullable=True)
    broker_user_id = db.Column(db.String(100), nullable=True)
    broker_pin = db.Column(db.String(100), unique=True, nullable=True)
    broker_qr_key =  db.Column(db.String(100), unique=True, nullable=True)
    broker_api =  db.Column(db.String(100), unique=True, nullable=True)
    broker_api_secret =  db.Column(db.String(100), unique=True, nullable=True)
    broker_password =  db.Column(db.String(100), unique=True, nullable=True)
    redirect_url = db.Column(db.String(100), unique=True, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=True)





    def __repr__(self):
        return f'<Broker {self.broker_name}>'