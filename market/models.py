from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('CourseName',backref='owned_user',lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self,pain_text_password):
        self.password_hash = bcrypt.generate_password_hash(pain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
class CourseName(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    batch = db.Column(db.String(length=30),nullable=False)
    regulartype = db.Column(db.String(length=30),nullable=False)
    cname = db.Column(db.String(length=30), nullable=False,unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self):
        return f'Item {self.studentname}' 
        