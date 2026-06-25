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
    if not user.active:
        return jsonify({"message": "Your account has been deactivated. Please contact the administrator."}), 403
    
    if not check_password_hash(user.password,data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

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
        "email": user.email,
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
            "status": trek.status,
            "staff_id": trek.staff_id 
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


#ADMIN VIEWING ALL USERS----------------------------------------------------------------------------------------------
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

#admin viewing all bookings___________________________________________________________________________________________
@app.route("/api/admin/bookings",methods=["GET"])
@jwt_required()
def all_bookings():
    admin = User.query.get(int(get_jwt_identity()))

    if admin.role != "admin":
        return {"message": "Unauthorized"}, 403
    bookings = Booking.query.all()
    result = []

    for booking in bookings:
        user = User.query.get(booking.user_id)
        trek = Trek.query.get(booking.trek_id)
        result.append({
            "booking_id": booking.id,
            "user": user.name,
            "trek": trek.name,
            "status": booking.status,
            "booking_date": booking.booking_date
        })

    return jsonify(result)





#admin deleteing users_---------------------------------------------------------------------------------------------
@app.route("/api/admin/user/<int:user_id>/deactivate",methods=["PUT"])
@jwt_required()
def deactivate_user(user_id):
    admin = User.query.get(int(get_jwt_identity()))

    if admin.role != "admin":
        return {"message": "Unauthorized"}, 403
    user = User.query.get(user_id)

    if not user:
        return {"message": "User not found"}, 404
    
    if user.role != "user":
        return {"message": "Selected account is not a user"}, 400
    
    user.active = False
    db.session.commit()
    return {"message": "User deactivated successfully"}



#admin deleting staff ___________________________________________________________________________________________________
@app.route("/api/admin/staff/<int:staff_id>/deactivate", methods=["PUT"])
@jwt_required()
def deactivate_staff(staff_id):
    admin = User.query.get(int(get_jwt_identity()))

    if admin.role != "admin":
        return {"message": "Unauthorized"}, 403

    staff = User.query.get(staff_id)
    if not staff:
        return {"message": "Staff not found"}, 404

    if staff.role != "staff":
        return {"message": "Selected account is not staff"}, 400
    
    staff.active = False
    db.session.commit()

    return {"message": "Staff deactivated successfully"}



#admin assigning staff to trek__________________________________________________________________________________________
@app.route("/api/admin/trek/<int:trek_id>/assign-staff", methods=["PUT"])
@jwt_required()
def assign_staff(trek_id):
    admin=User.query.get(int(get_jwt_identity()))
    if admin.role!="admin":
        return{"mesage":"unauthorised"},403
    data = request.get_json()
    trek = Trek.query.get(trek_id)
    if not trek:
        return{"message": "trek not found"},404
    staff = User.query.get(data["staff_id"])
    if not staff:
        return {"message": "Staff not found"}, 404
    if staff.role != "staff":
        return{"message":"Selected user is not a staff member"},400
    trek.staff_id = staff.id
    db.session.commit()
    return{"message":"staff assign successful"}
    

    
                         

#STAFF DASHBOARD ROUTE _-------------------------------------------------------------------------------------------
@app.route("/api/staff/treks", methods=["GET"])
@jwt_required()
def staff_treks():
    current_user = User.query.get(int(get_jwt_identity()))

    if current_user.role != "staff":
        return {"message": "Unauthorized"}, 403

    treks = Trek.query.filter_by(staff_id=current_user.id).all()

    result = []

    for trek in treks:
        result.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "status": trek.status,
            "slots": trek.available_slots
        })
    return jsonify(result)


#route for staff viewing participants ----------------------------------------------------------------------------

@app.route("/api/staff/participants/<int:trek_id>", methods=["GET"])
@jwt_required()
def view_participants(trek_id):
    current_user = User.query.get(int(get_jwt_identity()))

    if current_user.role != "staff":
        return {"message": "Unauthorized"}, 403

    trek = Trek.query.get(trek_id)

    if trek.staff_id != current_user.id:
        return {"message": "Not your trek"}, 403

    bookings = Booking.query.filter_by(trek_id=trek_id).all()

    result = []

    for booking in bookings:
        user = User.query.get(booking.user_id)
        result.append({
            "user_id": user.id,
            "name": user.name,
            "email": user.email
        })

    return jsonify(result)

#staff updating the trek status route_------------------------------------------------------------------------------------
@app.route("/api/staff/trek/<int:trek_id>",methods=["PUT"])
@jwt_required()
def update_trek_status(trek_id):

    current_user = User.query.get(int(get_jwt_identity()))

    if current_user.role != "staff":
        return {"message": "Unauthorized"}, 403

    trek = Trek.query.get(trek_id)

    if trek.staff_id != current_user.id:
        return {"message": "Not your trek"}, 403

    data = request.get_json()

    if "status" in data:
        trek.status = data["status"]

    if "available_slots" in data:
        trek.available_slots = data["available_slots"]

    db.session.commit()

    return {"message": "Updated"}

#updating the terk -----------------------------------------------------------------------------------------
@app.route("/api/admin/treks/<int:trek_id>", methods=["PUT"])
@jwt_required()
def update_trek(trek_id):
    admin = User.query.get(int(get_jwt_identity()))
    if admin.role != "admin":
        return {"message": "Unauthorized"}, 403
    trek = Trek.query.get(trek_id)
    if not trek:
        return {"message": "Trek not found"}, 404
    data = request.get_json()
    trek.name = data.get("name", trek.name)
    trek.location = data.get("location", trek.location)
    trek.difficulty = data.get("difficulty", trek.difficulty)
    trek.duration_days = data.get("duration_days", trek.duration_days)
    trek.available_slots = data.get("available_slots", trek.available_slots)
    trek.status = data.get("status", trek.status)
    trek.description = data.get("description", trek.description)

    if "start_date" in data:
        trek.start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")

    if "end_date" in data:
        trek.end_date = datetime.strptime(data["end_date"], "%Y-%m-%d")

    db.session.commit()
    return {"message": "Trek updated successfully"}


#deleting the trek______________________________________________________________________________________________________

@app.route("/api/admin/treks/<int:trek_id>", methods=["DELETE"])
@jwt_required()
def delete_trek(trek_id):
    admin = User.query.get(int(get_jwt_identity()))
    if admin.role != "admin":
        return {"message": "Unauthorized"}, 403
    trek = Trek.query.get(trek_id)
    if not trek:
        return {"message": "Trek not found"}, 404

    booking = Booking.query.filter_by(trek_id=trek.id).first()

    if booking:
        return {"message": "Cannot delete trek because users have already booked it."}, 400

    db.session.delete(trek)
    db.session.commit()
    return {"message": "Trek deleted successfully"}



#search bar------------------------------------------------------------------------------------------------------
@app.route("/api/search")
def search_treks():
    location = request.args.get("location")
    difficulty = request.args.get("difficulty")
    duration = request.args.get("duration")
    query = Trek.query
    if location:
        query = query.filter(Trek.location.ilike(f"%{location}%"))
    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)
    if duration:
        query = query.filter(Trek.duration_days == int(duration))

    treks = query.all()

    result = []

    for trek in treks:
        result.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration_days": trek.duration_days,
            "status": trek.status
        })

    return jsonify(result)

    


#update user profile rote_______________________________________________________________________________________________
@app.route("/api/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    user = User.query.get(int(get_jwt_identity()))
    data = request.get_json()

    user.name = data.get("name",user.name)

    db.session.commit()

    return {"message": "Profile updated successfully"}
    
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