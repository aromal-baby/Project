from flask import Flask, render_template, request,redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)


app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class User(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True)
    position = db.Column(db.String(100))
    company_name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    no_employees = db.Column(db.Integer)
    user_type = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


with app.app_context():
    db.create_all()




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        

        user = User.query.filter_by(email=username).first()

        if user and user.check_password(password):
            flash('Login successful!', 'success')
            return redirect(url_for('home'))

        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        first_name = request.form.get('frstname')
        last_name = request.form.get('lstname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        position = request.form.get('postn')
        company_name = request.form.get('cmpny')
        address = request.form.get('adrs')
        no_employees = request.form.get('empnum')
        password = request.form.get('password')
        cnf_password = request.form.get('cnfpass')


        user_id = f"{last_name.lower()}0000"
    

        if password != cnf_password:
            flash('Password do not match', 'error')
            return redirect(url_for('register'))


        try:
            new_user = User(
                user_id = user_id,
                first_name = first_name,
                last_name = last_name,
                phone = phone,
                email = email,
                position = position,
                company_name = company_name,
                address = address,
                no_employees = int(no_employees) if no_employees else None,
                user_type = "PERSONAL" if position else "INSTITUTE"
            )
            new_user.set_password(password)


            db.session.add(new_user)
            db.session.commit()

            flash('Registration already exists', 'error')
            return redirect(url_for('login'))

        except IntegrityError:
            db.session.rollback()
            flash('Email already exists', 'error')
            return redirect(url_for('register'))
                
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
            return redirect(url_for('register'))

    return render_template('/login')


@app.route('/')
def index():
    return render_template('UI.htm')

@app.route('/home')
def home():
    return render_template('UI.htm')


@app.route('/aboutUs')
def aboutUs():
    return render_template('AboutUs.htm')


if __name__ == '__main__':
    app.run(debug=True)
