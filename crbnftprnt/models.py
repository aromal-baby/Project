from crbnftprnt import db, app, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin #inherting from mixin class get access to many





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model):
    __tablename__ = 'users'

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