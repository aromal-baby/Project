from crbnftprnt import login_manager, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin #inherting from mixin class get access to many





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(UserMixin,db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
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

    def get_id(self):
        return self.user_id


class CrbnData(db.Model):

    __tablename__ = 'Crbndata'

    user_id = db.Column(db.String(100), db.ForeignKey('users.user_id'), primary_key=True)

    user = db.relationship('User', backref = db.backref('carbon_data', lazy=True, uselist=False))

    electric_bill = db.Column(db.Float)
    gas_bill = db.Column(db.Float)
    fuel_bill = db.Column(db.Float)
    waste_weight = db.Column(db.Float)
    recycled_val = db.Column(db.Float)
    dist_traveled = db.Column(db.Float)
    fuelef_avg = db.Column(db.Float)

    totalKgC02 = db.Column(db.Float)
    
