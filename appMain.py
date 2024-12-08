from flask import Flask, render_template, request,redirect, url_for


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('UI.htm')

@app.route('/home')
def home():
    return render_template('UI.htm')


@app.route('/aboutUs')
def aboutUs():
    return render_template('AboutUs.htm')


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # add the authentication logic here
    return f"Logged in as {username}"

 
@app.route('/register', methods=['GET', 'POST'])
def register():
    firstName = request.form.get('frstname')
    lastName = request.form.get('lstname')
    phone = request.form.get('phone')
    email = request.form.get('email')
    position = request.form.get('postn')
    company_name = request.form.get('cmpny')
    address = request.form.get('adrs')
    no_employees = request.form.get('empnum')
    password = request.form.get('password')
    cnfpassword = request.form.get('cnfpass')
    
    return f"Logged in as {firstName} {lastName} with details : {phone}{position}{company_name}{address}{no_employees} "



if __name__ == '__main__':
    app.run(debug=True)
