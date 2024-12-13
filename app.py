import os
import re
from crbnftprnt import app, db
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import secrets
from crbnftprnt.models import User
from flask_login import login_required


def validate_password(password):
    """
    Validate password strength
    """
    if len(password) < 8:
        return False
    
    if not re.search(r'[A-Z]', password):
        return False
    
    if not re.search(r'[a-z]', password):
        return False
    
    if not re.search(r'\d', password):
        return False
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
      
        return False
    return True

def generate_unique_user_id(last_name):
    """
    Generate a unique user ID
    """
    base_id = f"{last_name.lower()}{secrets.token_hex(2)}"
    return base_id



@app.route('/register', methods=['GET', 'POST'])
def register():
    # Get JSON data from request
    data = request.get_json()

    try:
        # Validate required fields
        if not all(key in data for key in ['frstname', 'lstname', 'email', 'password', 'cnfpass']):
            return jsonify({
                'success': False, 
                'message': 'All required fields must be filled'
            }), 400

        # Check password match
        if data['password'] != data['cnfpass']:
            return jsonify({
                'success': False, 
                'message': 'Passwords do not match'
            }), 400

        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({
                'success': False, 
                'message': 'Email already exists'
            }), 409

        # Generate unique user ID (you might want to implement a more robust method)
        user_id = f"{data['lstname']}_{User.query.count() + 1}"

        # Create new user
        new_user = User(
            user_id=user_id,
            first_name=data['frstname'],
            last_name=data['lstname'],
            phone=data.get('phone', ''),
            email=data['email'],
            user_type=data.get('userType', 'PERSONAL')
        )

        # Set password
        new_user.set_password(data['password'])

        # Add institute-specific details if available
        if data.get('userType') == 'INSTITUTE':
            new_user.position = data.get('postn', '')
            new_user.company_name = data.get('cmpny', '')
            new_user.address = data.get('adrs', '')
            new_user.no_employees = int(data.get('empnum', 0)) if data.get('empnum') else None

        # Add to database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'success': True, 
            'message': 'Registration successful',
            'user_id': user_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False, 
            'message': f'Registration failed: {str(e)}'
        }), 500
    



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:

            if request.is_json:
                data = request.get_json()
            else:
                data = request.form

            username = data.get('username')
            password = data.get('password')
            

            print(f"Login attempt for username: {username}")

            user = User.query.filter_by(email=username).first()

            if user and user.check_password(password):

                return jsonify({
                    'message': 'Login successful',
                    'redirect': url_for('main_cont')
                }), 200 
            else:
                return jsonify({
                    'errorMessage': 'Invalid email or password'
                }), 401
        
        except Exception as e:

            print(f"Login error: {str(e)}")
            return jsonify({
                'errorMessage': 'An unexpected error occurred'
            }), 500

    return render_template('main-cont.html')


@app.route('/')
def index():
    return render_template('index.htm')

@app.route('/home')
def home():
    return render_template('index.htm')

@app.route('/aboutUs')
def aboutUs():
    return render_template('AboutUs.htm')

@app.route('/main-content')
@login_required
def main_cont():

    return render_template('main-cont.html')

@app.route('/register-page')
def register_form():
    return render_template('register.html')


if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database created successfully")
        except Exception as e:
            print(f"Error creating database: {e}")
    
    app.run(debug=True)