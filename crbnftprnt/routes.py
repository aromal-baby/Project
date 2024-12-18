from crbnftprnt import app, db, logger
from flask import render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from crbnftprnt.models import User, CrbnData
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import os, re, traceback, base64, secrets

def validate_password(password):

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

                login_user(user)
                return jsonify({
                    'success': True,
                    'message': 'Login succsessful',
                    'redirect': url_for('main_cont')
                }), 200
            
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid email or password'
                }), 401
             
        except Exception as e:
            print(f"Login error: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'An unexpected error occurred'
            }), 500

    return render_template('main-cont.html')


@app.route('/main-content', methods = ['GET', 'POST'])
@login_required
def main_cont():

    if request.method == 'GET':
        return render_template('main-cont.html')

    try :

        if not current_user.is_authenticated:
            logger.error("User not authenticated")
            return jsonify({"error": "User not authenticated"}), 401

        user = User.query.filter_by(user_id=current_user.user_id).first()
        if not user:
            logger.error(f"User not found: {current_user.user_id}")
            return jsonify({"error": "User not found"}), 404


        if not request.is_json:
            logger.error("Request must be JSON")
            return jsonify({"error": "Request must be JSON"}), 400
            
        print("Recieved data:", request.get_json())
        return handle_post_request(user)
        
    except Exception as e :
        logger.error(f"Unexpected error occured in main_cont: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": {str(e)}}), 500
    


def handle_post_request(user):
    
    try:
        logger.info("Received POST request to /main-content")

        data = request.get_json()
        logger.info(f"Recieved data: {data}")

        if not data:
            logger.error("No input data provided")
            return jsonify({"error": "No input data provided"}), 400

        validated_data = validate_input_data(data)
        if validated_data is None:
            logger.error("Data validation failed")
            return jsonify({"error": "Invalid input data"}), 400

        logger.info(f"Validation data: {validated_data}")

        try:
            carbon_emission_result = calculate_and_save_emission(validated_data, user.no_employees)
            logger.info(f"Calculation result: {carbon_emission_result}")
        except Exception as e:
            logger.info(f"Error in calculation: {str(e)}")
            return jsonify({"error": "Error calculating emissions: {str(e)}"}), 500

        try:
            graph_base64 = generate_emission_graph(carbon_emission_result)
            if graph_base64 is None:
                raise Exception("Graph generation returned None")
        except Exception as e:
            logger.error(f"Graph genration error: {str(e)}")
            return jsonify({"errror": "Error generating graph {str(e)}"}), 500

        response_data = {
            'total_carbon_emission_by_energy': carbon_emission_result['total_carbon_emission_by_energy'],
            'total_carbon_emission_by_waste': carbon_emission_result['total_carbon_emission_by_waste'],
            'total_carbon_emission_by_business': carbon_emission_result['total_carbon_emission_by_business'],
            'graph': graph_base64
        }
        logger.info("Successfully prepared response data")
        return jsonify(response_data), 200

    except Exception as e:
        logger.error(f"HAndle post reequest error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": "An unexpected error occurred: {str(e)}" 
        }), 500

            
def validate_input_data(data):
    try:
       validated_data = {
            'electric_bill': float(data.get('electricbill', 0) or 0),
            'gas_bill': float(data.get('gasbill', 0) or 0),
            'fuel_bill': float(data.get('fuelbill', 0) or 0),
            'waste_weight': float(data.get('wstweight', 0) or 0),
            'recycled_val': float(data.get('recycled_perc', 0) or 0),
            'dist_traveled': float(data.get('distance_traveled', 0) or 0),
            'fuelef_avg': float(data.get('fuelef_avg', 0) or 0)
        }
       return validated_data
    
    except (TypeError, ValueError) as e:
        logger.error(f"Input validation error: {e}")
        return None

def calculate_and_save_emission(data, employee_count):
    try:
        employee_count = employee_count or 1
        carbon_emission_result = calculate_carbon_emission(data, employee_count)
        save_carbon_data_to_db(carbon_emission_result['total_carbon_emission'])
        return carbon_emission_result
    except Exception as e:
        print(f"Error during calculation or saving: {e}")
        raise


def calculate_carbon_emission(data, employee_count):

    try:
        logger.info(f"calculating emmissions with data: {data}, employee_count: {employee_count}")

        total_carbon_emission_by_energy = (
            (float(data['electric_bill']) * 12 * 0.0005) + 
            (float(data['gas_bill']) * 12 * 0.0053) + 
            (float(data['fuel_bill']) * 12 * 2.32)
        )

        total_waste = data['waste_weight'] 
        recycled_waste = (total_waste * data['recycled_val']) / 100
        non_recycled_waste = total_waste - recycled_waste

        total_carbon_emission_by_waste = (non_recycled_waste) * 12 * 0.57 

        total_carbon_emission_by_business = (
            float(data['dist_traveled']) * 
            float(employee_count) * 
            (1 / float(data['fuelef_avg'])) * 2.31
        ) if float(data['fuelef_avg']) != 0 else 0

        result = {
            'total_carbon_emission_by_energy': total_carbon_emission_by_energy,
            'total_carbon_emission_by_waste': total_carbon_emission_by_waste,
            'total_carbon_emission_by_business': total_carbon_emission_by_business,
            'total_carbon_emission': (
                total_carbon_emission_by_energy +
                total_carbon_emission_by_waste +
                total_carbon_emission_by_business
            )
        }
        
        logger.info(f"Calculation result: {result}")
        return result

    except Exception as e:
        logger.error(f"Error in calculate_carbon_emission: {str(e)}")
        raise


def save_carbon_data_to_db(total_carbon_emission):
 
    try:
        carbon_data = CrbnData(totalKgC02=total_carbon_emission)
        db.session.add(carbon_data)
        db.session.commit()
    except Exception as e:
        print(f"Database error: {e}")
        db.session.rollback()


def generate_emission_graph(carbon_emission_result):

    try:

        logger.info(f"Generating graph with data: {carbon_emission_result}")

        plt.figure(figsize=(8, 6), dpi=100)

        values = [
            max(0, carbon_emission_result['total_carbon_emission_by_energy']), 
            max(0, carbon_emission_result['total_carbon_emission_by_waste']), 
            max(0, carbon_emission_result['total_carbon_emission_by_business'])
        ]

        logger.info(f"plotting values: {values}")

        if sum (values) == 0:
            values = [0.1, 0.1, 0.1]

        labels = ['Energy Consumption', 'Waste Emission', 'Business Travel']
        colors = ['red', 'green', 'blue']

        plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title('Carbon Emission Distribution')
       
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)

        image_bytes = buffer.getvalue()
        encoded = base64.b64encode(image_bytes)
        image_base64 = encoded.decode('utf-8')
        

        buffer.close()
        plt.clf()

        logger.info("Succesfully generated graph")
        return image_base64
       
    except Exception as e:
        logger.error(f"Error in generate_emission_graph: {str(e)}")
        return None



@app.route('/')
def index():
    return render_template('index.htm')

@app.route('/home')
def home():
    return render_template('index.htm')

@app.route('/aboutUs')
def aboutUs():
    return render_template('AboutUs.htm')

@app.route('/register-page')
def register_form():
    return render_template('register.html')


