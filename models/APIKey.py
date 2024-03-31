from app import db

class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_name = db.Column(db.String(50), nullable=False)
    key_value = db.Column(db.String(256), nullable=False)
    model_type = db.Column(db.String(20), nullable=False)