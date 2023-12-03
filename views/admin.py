from models.customer import Customer
from models.reservation import Reservation
from config.db_config import get_db

class adminView:
    def __init__(self):
        self.db = get_db()
        self.customers=self.db.customers
        self.reservations = self.db.reservations
    
    def adminData(self):
        customers_collection = self.customers
        reservations_collection = self.reservations
        
        customers = list(customers_collection.find())
        customer_reservations = []

        for customer in customers:
            # Find all reservations for this customer
            reservations = list(reservations_collection.find({"customerId": customer["customerId"], "seated": {"$ne": True}, "canceled": {"$ne": True}}))
            if reservations:
                customer_data = {
                    "username": customer["username"],
                    "name": customer.get("name", ""),
                    "email": customer.get("email", ""),
                    "seated": customer.get("seated", False),
                    "reservations": reservations
                }
#               if not all(reservation.get("seated", False) for reservation in reservations):
                customer_reservations.append(customer_data)
        
        print("Filtered Customer Reservations:", customer_reservations)
        return customer_reservations    

    
    def update_customer_status(self, customer_username, reservation_id):
        result_customer = self.customers.update_one({"username": customer_username}, {"$set": {"seated": True}})
 
        print(f"result modified is {result_customer.modified_count}")
        if result_customer.modified_count >= 0:
            # Check if the reservation exists
            reservation = self.reservations.find_one({"reservationId": reservation_id})
            if reservation:
                print(f"Updating reservation status for {reservation_id}")
                filter = {"reservationId": reservation_id}
                update = {"$set": {"seated": True}}
                result_reservation = self.reservations.update_one(filter, update)
                print(f"Filter: {filter}, Update: {update}")

 #              result_reservation = self.reservations.update_one({"reservationId": reservation_id}, {"$set": {"seated": True}})
                print(f"Result for reservation update: {result_reservation.modified_count} document(s) modified")

                if result_reservation.modified_count > 0:
                    return {"success": True, "message": f"Customer {customer_username} status and reservation {reservation_id} marked as seated successfully."}
                else:
                    return {"success": False, "message": f"Failed to update reservation {reservation_id} status."}
        else:
            return {"success": False, "message": f"Failed to update customer {customer_username} status."}

    def cancel_reservation(self, customer_username, reservation_id):
        # Update reservation status to canceled
        print(f"Canceling reservation status for {reservation_id} and username {customer_username}")
        reservation = self.reservations.find_one({"reservationId": reservation_id})
        print(f"reservation is {reservation}")
        if reservation:
            result_reservation = self.reservations.update_one(
                {"reservationId": reservation_id},
                {"$set": {"canceled": True}}
            )

            if result_reservation.modified_count > 0:
                return {"success": True, "message": f"Reservation {reservation_id} canceled successfully."}
            else:
                return {"success": False, "message": f"Failed to cancel reservation {reservation_id}."}

    def remove_all_customers(self):
        customers_collection = self.customers
        reservations_collection = self.reservations

        # Remove all customers
        result_customers_removed = customers_collection.delete_many({})
        result_reservations_removed = reservations_collection.delete_many({})
        if result_customers_removed.deleted_count > 0 and result_reservations_removed.deleted_count > 0:
            return {"success": True, "message": "All customers removed successfully"}
        else:
            return {"success": False, "message": "No customers found to remove"}
        
