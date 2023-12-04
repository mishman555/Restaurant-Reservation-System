from models.customer import Customer
from models.reservation import Reservation
from config.db_config import get_db

class adminView:
    """
    A class representing the view and actions of an admin in the restaurant reservation system.

    Attributes:
    - db: Database instance.
    - customers: Collection of customer documents in the database.
    - reservations: Collection of reservation documents in the database.
    """
    def __init__(self):
        """
        Initialize an AdminView instance with a connection to the database.
        """
        self.db = get_db()
        self.customers=self.db.customers
        self.reservations = self.db.reservations
    
    def adminData(self):
        """
        Retrieve customer reservations for admin display.

        Returns:
        list: List of dictionaries containing customer data and their reservations.
        """
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
                customer_reservations.append(customer_data)
        
        return customer_reservations    

    def update_customer_status(self, customer_username, reservation_id):
        """
        Update the seated status of a customer and their reservation.

        Parameters:
        - customer_username (str): Username of the customer.
        - reservation_id (int): ID of the reservation.

        Returns:
        dict: Dictionary indicating the success or failure of the operation.
        """
        result_customer = self.customers.update_one({"username": customer_username}, {"$set": {"seated": True}})
 
        if result_customer.modified_count >= 0:
            # Check if the reservation exists
            reservation = self.reservations.find_one({"reservationId": reservation_id})
            if reservation:
                filter = {"reservationId": reservation_id}
                update = {"$set": {"seated": True}}
                result_reservation = self.reservations.update_one(filter, update)

                if result_reservation.modified_count > 0:
                    return {"success": True, "message": f"Customer {customer_username} status and reservation {reservation_id} marked as seated successfully."}
                else:
                    return {"success": False, "message": f"Failed to update reservation {reservation_id} status."}
        else:
            return {"success": False, "message": f"Failed to update customer {customer_username} status."}

    def cancel_reservation(self, customer_username, reservation_id):
        """
        Cancel a reservation by updating its status.

        Parameters:
        - customer_username (str): Username of the customer.
        - reservation_id (int): ID of the reservation.

        Returns:
        dict: Dictionary indicating the success or failure of the operation.
        """

        reservation = self.reservations.find_one({"reservationId": reservation_id})

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
        """
        Remove all customers and their reservations from the database.

        Returns:
        dict: Dictionary indicating the success or failure of the operation.
        """
        customers_collection = self.customers
        reservations_collection = self.reservations

        result_customers_removed = customers_collection.delete_many({})
        result_reservations_removed = reservations_collection.delete_many({})
        if result_customers_removed.deleted_count > 0 and result_reservations_removed.deleted_count > 0:
            return {"success": True, "message": "All customers removed successfully"}
        else:
            return {"success": False, "message": "No customers found to remove"}
        
