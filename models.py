from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    role = db.Column(db.String(20),default="user")
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship("Booking", backref="user", lazy=True)


class Trek(db.Model):
    __tablename__ = "treks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    difficulty = db.Column(db.String(20))
    duration_days = db.Column(db.Integer)
    available_slots = db.Column(db.Integer)
    status = db.Column(db.String(20))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    bookings = db.relationship("Booking", backref="trek", lazy=True)


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"))
    booking_date = db.Column(db.DateTime, default=datetime.utcnow )
    status = db.Column(db.String(20), default="Booked")
    payment_status = db.Column(db.String(20), default="Pending")