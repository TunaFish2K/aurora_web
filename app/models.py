from flask_login import UserMixin
from . import db
from . import login_manager
from werkzeug.security import generate_password_hash,check_password_hash

class User(UserMixin,db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True)
    password_hash=db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError("Password is not readable.")
    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


    def __repr__(self):
        return '<Role {}>'.format(self.name)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))