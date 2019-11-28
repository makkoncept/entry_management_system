from datetime import datetime
from entrymanagement import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Host.query.get(int(user_id))


class Host(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_no = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100), nullable=False, default="dehradun, india")
    password_hash = db.Column(db.String(60), nullable=False)

    guest = db.relationship("GuestCheckIn", backref="guest", lazy=True)

    def __repr__(self):
        return f"Host('{self.username}', '{self.email}')"


class GuestCheckIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guestname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_no = db.Column(db.String(10), nullable=False)
    checkin_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    checkout_timestamp = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey("host.id"), nullable=False)

    def __repr__(self):
        return f"Guest('{self.guestname}', '{self.email}')"
