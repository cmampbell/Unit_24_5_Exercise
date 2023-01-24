from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.VARCHAR(length=20), primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.VARCHAR(length=50), nullable=False)
    first_name = db.Column(db.VARCHAR(length=30), nullable=False)
    last_name = db.Column(db.VARCHAR(length=30), nullable=False)

    feedback = db.relationship('Feedback', backref='user')

    def __repr__(self):
        u = self
        return f"<Username: {u.username}, Password: {u.password} Email: {u.email}, First Name: {u.first_name}, Last Name: {u.last_name}"
    
    def serialize(self):
        return {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'feedback': self.feedback
        }

    @classmethod
    def register(cls, data):
        user_info = {**data}

        pw_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        return cls(username=user_info['username'], password=pw_hash, email=user_info['email'], 
                   first_name=user_info['first_name'], last_name=user_info['last_name'])
    
    @classmethod
    def login(cls, data):
        user = User.query.get(data['username'])
        if user and bcrypt.check_password_hash(user.password, data['password']):
            return user
        else:
            raise #should return a specific error here

class Feedback(db.Model):

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.VARCHAR(length=100), nullable=False)
    content = db.Column(db.String, nullable=False)
    username = db.Column(db.VARCHAR(length=20), db.ForeignKey('users.username', ondelete='cascade'))

    @classmethod
    def create_feedback(cls, data, username):
        feedback_info = {**data}
        return cls(title=feedback_info['title'], content=feedback_info['content'], username=username)