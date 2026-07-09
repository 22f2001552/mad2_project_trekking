import csv
from backend.celery_app import celery
from backend.celery_utils import create_app
from backend.models import Booking, Trek, User
from datetime import date




@celery.task
def export_booking_csv(user_id):
    app = create_app()
    with app.app_context():
        bookings = Booking.query.all()
        filename = "all_bookings.csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Booking ID",
                "User",
                "Trek Name",
                "Location",
                "Booking Date",
                "Status"
                ])
            
            for booking in bookings:
                trek = Trek.query.get(booking.trek_id)
                user = User.query.get(booking.user_id)
                writer.writerow([
                    booking.id,
                    user.name,
                    trek.name,
                    trek.location,
                    booking.booking_date,
                    booking.status
                ])
                
        return filename
    


@celery.task
def daily_reminder():
    app = create_app()
    with app.app_context():
        today = date.today()
        bookings = Booking.query.all()
        for booking in bookings:
            trek = Trek.query.get(booking.trek_id)
            user = User.query.get(booking.user_id)
            if trek.start_date == today:
                print("=" * 50)
                print(f"Reminder for {user.name}")
                print(f"Trek : {trek.name}")
                print(f"Location : {trek.location}")
                print("Starts Today!")
                print("=" * 50)
    return "Daily reminder completed"



@celery.task
def monthly_report():
    app = create_app()
    with app.app_context():
        total_users = User.query.count()
        total_treks = Trek.query.count()
        total_bookings = Booking.query.count()
        print("\n========== MONTHLY REPORT ==========")
        print(f"Total Users : {total_users}")
        print(f"Total Treks : {total_treks}")
        print(f"Total Bookings : {total_bookings}")
        print("====================================\n")

    return "Monthly report generated"



