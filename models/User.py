# models/User.py
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(256), nullable=False)

    # Relations
    api_keys = db.relationship('APIKey', backref='user', lazy=True)
    query_history = db.relationship('QueryHistory', backref='user', lazy=True)

    @property
    def is_active(self):
        # This should return True if the user's account is active.
        # For this example, we'll always return True.
        return True

    @property
    def is_authenticated(self):
        # This should return True if the user is authenticated, i.e., they have provided valid credentials.
        # For this example, we'll always return True.
        return True

    def get_id(self):
        """
        Return the email to satisfy Flask-Login's requirements.
        """
        return str(self.id)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)