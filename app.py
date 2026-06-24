from flask import Flask
from config import Config
from models import db, User,Trek,Booking
from flask import request, jsonify
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from models import User
from flask_jwt_extended import (JWTManager,create_access_token,jwt_required,get_jwt_identity)
from datetime import datetime



app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

jwt = JWTManager(app)

@app.route("/")
def home():
    return "Trekking Management API Running!"




#registration route-------------------------------------------------------------------------
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    existing = User.query.filter_by(email=data["email"]).first()

    if existing:
        return jsonify({"message": "Email already exists"}), 400

    user = User(
        name=data["name"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role="user"
    )

    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered"})      







#login route___________________________________________________________________________________________
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401
    
    if not check_password_hash(user.password,data["password"]):
        return jsonify({
            "message": "Invalid credentials"
        }), 401

    token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "token": token,
        "role": user.role,
        "name": user.name
        })

#profile route__________________________________________________________________________________________________________________
@app.route("/api/profile")
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    return jsonify({
        "id": user.id,
        "name": user.name,
        "role": user.role
    })


    

#CREATE STAFF ROUTE ______________________________________________________________________________________________________
@app.route("/api/admin/staff", methods=["POST"])
@jwt_required()
def create_staff():
    current_user_id = get_jwt_identity()
    admin = User.query.get(current_user_id)
    if admin.role != "admin":
        return {"message": "Unauthorized"}, 403
    data = request.get_json()
    existing = User.query.filter_by(email=data["email"]).first()
    if existing:
        return {"message": "Email already exists"}, 400
    
    staff = User(
        name=data["name"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role="staff"
    )

    db.session.add(staff)
    db.session.commit()
    return {"message": "Staff created"}

#creatre trekk route____________________________________________________________________________________________________
@app.route("/api/admin/treks", methods=["POST"])
@jwt_required()
def create_trek():

    current_user_id = get_jwt_identity()

    admin = User.query.get(current_user_id)

    if admin.role != "admin":
        return {"message": "Unauthorized"}, 403

    data = request.get_json()

    trek = Trek(
        name=data["name"],
        location=data["location"],
        difficulty=data["difficulty"],
        duration_days=data["duration_days"],
        available_slots=data["available_slots"],
        status="Open",
        start_date=datetime.strptime(
            data["start_date"],
            "%Y-%m-%d"
        ),
        end_date=datetime.strptime(
            data["end_date"],
            "%Y-%m-%d"
        ),
        staff_id=data["staff_id"]
    )

    db.session.add(trek)
    db.session.commit()

    return {"message": "Trek created"}

#view trekk---------------------------------------------------------------------------------------------------------------
@app.route("/api/treks", methods=["GET"])
def get_treks():

    treks = Trek.query.all()

    result = []

    for trek in treks:

        result.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "slots": trek.available_slots,
            "status": trek.status
        })

    return result

#book trekk_______________________________________________________________________________________________________________
@app.route("/api/bookings", methods=["POST"])
@jwt_required()
def book_trek():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    trek = Trek.query.get(data["trek_id"])

    if not trek:
        return {"message": "Trek not found"}, 404

    if trek.status != "Open":
        return {"message": "Trek not open"}, 400

    if trek.available_slots <= 0:
        return {"message": "No slots available"}, 400

    existing = Booking.query.filter_by(
        user_id=user_id,
        trek_id=trek.id
    ).first()

    if existing:
        return {"message": "Already booked"}, 400

    booking = Booking(user_id=user_id,trek_id=trek.id)

    trek.available_slots -= 1

    db.session.add(booking)
    db.session.commit()

    return {"message": "Booking successful"}


#users view booking route_____________________________________________________________________________________________________
@app.route("/api/my-bookings", methods=["GET"])
@jwt_required()
def my_bookings():
    user_id = int(get_jwt_identity())
    bookings = Booking.query.filter_by(user_id=user_id).all()
    result = []
    for booking in bookings:
        trek = Trek.query.get(booking.trek_id)
        result.append({
            "booking_id": booking.id,
            "trek_name": trek.name,
            "location": trek.location,
            "status": booking.status
        })

    return jsonify(result)


#ADMIN VIEWING ALL USERS--------------------------------------------------------------
@app.route("/api/admin/users")
@jwt_required()
def all_users():
    current_user = User.query.get(int(get_jwt_identity()))
    if current_user.role != "admin":
        return {"message": "Unauthorized"}, 403
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        })

    return jsonify(result)


#admin viewing all staff____________________________________________________________________________________________

@app.route("/api/admin/staff")
@jwt_required()
def all_staff():
    current_user = User.query.get(int(get_jwt_identity()))
    if current_user.role != "admin":
        return {"message": "Unauthorized"}, 403

    staff = User.query.filter_by(role="staff").all()
    result = []
    for s in staff:
        result.append({
            "id": s.id,
            "name": s.name,
            "email": s.email
        })

    return jsonify(result)

#----------------------------------------------------------------------------------------------------------------------

with app.app_context():
    db.create_all()
    admin = User.query.filter_by(role="admin").first()

    if not admin:
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password=generate_password_hash("admin123"),
            role="admin"
    )
        db.session.add(admin)
        db.session.commit()
        print("Admin created")

if __name__ == "__main__":
    app.run(debug=True)