# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mob_no = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    conf_pass = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.fullname}>'
