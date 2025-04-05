from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    records = db.relationship('DeliveryRecord', backref='driver', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class DeliveryRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True, default=datetime.utcnow)
    time = db.Column(db.String(5), nullable=False)  # HH:MM format
    description = db.Column(db.String(200), nullable=True)  # Сделали nullable
    quantity = db.Column(db.Integer, nullable=True)         # Сделали nullable
    amount = db.Column(db.Float, nullable=True)             # Сделали nullable
    payment_type = db.Column(db.String(20), nullable=True)  # Сделали nullable
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.Column(db.Text, nullable=True)                # Добавлено поле для заметки
    is_note = db.Column(db.Boolean, default=False, nullable=False)  # Добавлено поле для флага

    def __repr__(self):
        return f'<DeliveryRecord {self.id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
