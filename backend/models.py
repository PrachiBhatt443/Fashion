# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash

# db = SQLAlchemy()

# # User model for storing user data
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     role = db.Column(db.String(50), nullable=False)

#     def set_password(self, password):
#         self.password = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password, password)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")
    name = db.Column(db.String(255), nullable=False)
    education = db.Column(db.String(255))
    photo = db.Column(db.String(255))  # Add this field for storing photo filename
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
