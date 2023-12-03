from models.reservation import Reservation
from config.db_config import get_db

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class reservationView:
    def __init__(self,username=None, reservationId=None, number_of_seats=None, reservation_date=None):
        self.username = str(username)
        self.reservationId = reservationId
        self.number_of_seats = number_of_seats
        self.reservation_date = reservation_date
        self.db = get_db()

    def send_email(self, recipient_email, subject, body):
        # Gmail email configuration
        sender_email = "restaurantreservationsbing@gmail.com"  # Replace with your Gmail address
        app_password = "zmda carx cmxs roqr"  # Replace with your Gmail App Password

        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        # Attach body to the message
        message.attach(MIMEText(body, "plain"))

        # Connect to Gmail's SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Use TLS (Transport Layer Security)
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
    
    def insert(self):
        try:
            reservations_collection = self.db.reservations
            customers_collection = self.db.customers
            user = customers_collection.find_one({"username": self.username})
            print(f"CustomerID is {user['customerId']}")
            reservation = Reservation(
            customerId = user["customerId"],
            reservationId = self.reservationId,
            number_of_seats = self.number_of_seats,
            reservation_date = self.reservation_date
            )
            result = reservations_collection.insert_one(reservation.to_dict())

            if result.inserted_id:
                # Send email notification
                subject = "Reservation Confirmed"
                body = f"Your reservation has been confirmed. Reservation ID: {self.reservationId}, Seats: {self.number_of_seats}, Date: {self.reservation_date}"
                self.send_email(user["email"], subject, body)

                return {"success": True, "message": "Reservation made successfully"}
            else:
                return {"success": False, "message": "Failed to add customer"}
        
        except Exception as e:
            return {"success": False, "message": f"An error occurred: {e}"}
        

    
    def find(self):
        reservations_collection = self.db.reservations
        reservation_details = reservations_collection.find_one({"reservationId": self.reservationId})
        return reservation_details
