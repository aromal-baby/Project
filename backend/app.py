from flask import Flask, request, jsonify
import mysql.connector
import bcrypt 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host = ',localhost',
        user = 'root',
        password = 'root',
        database = 'crbnftprnt_db'
    )

@app.route('/register', methods = ['POST'])
def register_user():
    try:
        data = request.get_json()
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        password = data.get('hashedPass')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.genssalt())

        conn = get_db_connection()
        cursor = con.cursor()

        query = """
                INSERT INTO users (first_name, last_name, email, password_hash)
                VALUES (%s, %s, %s, %s)
                """
        
        cursor.execute(query(first_name, last_name, email, hashed_password))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message:" "User registered successfully"}),201
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}),500
    
@app.route('/login', methods = ['POST'])
def login_user():
    try :
        data = requwest.get_json()
        email = data.get('email')
        password = data.get('password')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email = %s', (email))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error" : "Invalid email or password!"}),400
        
        stored_hash = user[4]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            cursor.close()
            conn.close()
            return jsonify({"message": "Login successful!"}), 200
        else :
            cursor.close()
            conn.close()
            return jsonify({"error" : "Invalid email or password!"})
    except exception as e:
        return jsonify({"error": f"Error: {str(e)}"}),500

if __name__== '__main__':
    app.run(debug= True, host = '0.0.0.0, port=5000')


 