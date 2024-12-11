import os
import re
from crbnftprnt import app, db
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import secrets
from crbnftprnt.models import User


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
    if request.method == 'POST':

        if request.is_json:
            data = request.get_json()

        else :
            data = request.form


        first_name = data.get('frstname') or request.form.get('frstname')
        last_name = data.get('lstname') or request.form.get('lstname')
        phone = data.get('phone') or request.form.get('phone')
        email = data.get('email') or request.form.get('email')
        position = data.get('postn') or request.form.get('postn')
        company_name = data.get('cmpny') or request.form.get('cmpny')
        address = data.get('adrs') or request.form.get('adrs')
        no_employees = data.get('empnum') or request.form.get('empnum')
        password = data.get('password') or request.form.get('password')
        cnf_password = data.get('cnfpass') or request.form.get('cnfpass')


        if not all([first_name, last_name, email, password, cnf_password]):
            flash('All required feilds must be filled', 'error')
            return redirect(url_for('register'))

        # Validate password match
        if password != cnf_password:
           flash('Passwords do not match')
           return redirect(url_for('register'))

        # Validate password strength
        if not validate_password(password):
            flash('Password does not meet strength requirements')
            return redirect(url_for('register'))

        # Generate unique user ID
        user_id = generate_unique_user_id(last_name)

        try:
            # Check if email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already exists')
                return redirect(url_for('register'))
            

            new_user = User(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                position=position,
                company_name=company_name,
                address=address,
                no_employees=int(no_employees) if no_employees else None,
                user_type="PERSONAL" if position else "INSTITUTE"
            )
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            flash(f'Registration successful!', 'success')
            return redirect(url_for('main_cont'))

        except IntegrityError:
            db.session.rollback()
            flash(f'Email aready exist! Please login')
            return render_template('index.htm')


        except Exception as e:
            db.session.rollback()
            flash(f'Register failed: {str(e)}', 'error')
            return redirect(url_for('register'))

    flash(f'registration successful! Please login ')
    return render_template('login.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        if request.is_json:
            data = request.get_json()

        else :
            data = request.form


        username = data.get('username') or request.form.get('username') 
        password = data.get('password') or request.form.get('password') 

        user = User.query.filter_by(email=username).first()

        if user and user.check_password(password):
          return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))

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