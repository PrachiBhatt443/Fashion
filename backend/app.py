import os
# from backend.extract import get_color_data
from extract import get_color_data
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from werkzeug.utils import secure_filename
from models import db, User
from config import Config

app = Flask(__name__)

# CORS setup for cross-origin requests (between React and Flask)
CORS(app)

# App configuration
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'uploads/photos'  # Add this to configure the upload folder
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/users/register', methods=['POST'])
def register():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    role = request.form.get('role', 'user')
    name = request.form.get('name', None)
    education = request.form.get('education', None)
    
    photo = request.files.get('photo')  # Retrieving the photo file
    
    if not email or not password or not name:
        return jsonify({"message": "Email, password, and name are required!"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists!"}), 400

    if photo and allowed_file(photo.filename):
        # Save the photo
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = None  # Default if no photo uploaded
    
    # Create new user
    user = User(email=email, role=role, name=name, education=education, photo=filename)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
@app.route('/api/users/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email or not password:
        return jsonify({"message": "Email and password are required!"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):  # Assuming you have check_password method in User model
        access_token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful", "access_token": access_token}), 200

    return jsonify({"message": "Invalid email or password"}), 401

@app.route('/api/colors', methods=['GET'])
def get_colors():
    folder_path = 'datasets'  
    color_data = get_color_data(folder_path)  
    return jsonify(color_data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
