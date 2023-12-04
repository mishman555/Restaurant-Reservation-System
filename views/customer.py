from models.customer import Customer
from config.db_config import get_db

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class customerView:
    """
    A class representing the view and actions of a customer in the restaurant reservation system.
    """
    def __init__(self,customerId=None,username=None,name=None,address=None,phoneNumber=None,email=None, seated=False):
        """
        Initialize a CustomerView instance with customer information and a connection to the database.

        Attributes:
        - customerId (str): ID of the customer.
        - username (str): Username of the customer.
        - name (str): Name of the customer.
        - address (str): Address of the customer.
        - phoneNumber (str): Phone number of the customer.
        - email (str): Email address of the customer.
        - seated (bool): Seated status of the customer.
        - db: Database instance.
        """
        self.customerId=customerId
        self.username=username
        self.name=name
        self.address=address
        self.phoneNumber=phoneNumber
        self.email=email
        self.seated = seated
        self.db = get_db()

    def send_email(self, subject, body):
        """
        Send an email to the customer.

        Parameters:
        - subject (str): Subject of the email.
        - body (str): Body of the email.
        """
        # Email configuration
        sender_email = "restaurantreservationsbing@gmail.com"
        sender_password = "zmda carx cmxs roqr"
        receiver_email = self.email

        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Attach body to the message
        message.attach(MIMEText(body, "plain"))

        # Connect to Gmail SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            # Log in to your Gmail account
            server.login(sender_email, sender_password)
            # Send the email
            server.sendmail(sender_email, receiver_email, message.as_string())

    
    def insert(self):
        """
        Insert a new customer into the database.

        Returns:
        dict: Dictionary indicating the success or failure of the operation.
        """
        try:
            customers_collection = self.db.customers
            customer = Customer(
                customerId=self.customerId,
                username=self.username,
                name=self.name,
                address=self.address,
                phoneNumber=self.phoneNumber,
                email=self.email,
                seated=self.seated
            )

            result = customers_collection.insert_one(customer.to_dict())

            if result.inserted_id:
                # Send email notification
                subject = "Customer Added Successfully"
                body = "Thank you for registering with us!"
                self.send_email(subject, body)

                return {"success": True, "message": "Customer added successfully"}
            else:
                return {"success": False, "message": "Failed to add customer"}
        
        except Exception as e:
            # Handle any exceptions that occur during the insert
            return {"success": False, "message": f"An error occurred: {e}"}
    
    def update_customer_status(self, customer_id, seated=True):
        """
        Update the seated status of a customer.

        Parameters:
        - customer_id (str): ID of the customer.
        - seated (bool): New seated status.

        Returns:
        dict: Dictionary indicating the success or failure of the operation.
        """
        try:
            customers_collection = self.db.customers
            result = customers_collection.update_one(
                {"customerId": customer_id},
                {"$set": {"seated": seated}}
            )

            if result.modified_count > 0:
                return {"success": True, "message": "Customer status updated successfully"}
            else:
                return {"success": False, "message": "Failed to update customer status"}

        except Exception as e:
            return {"success": False, "message": f"An error occurred: {e}"}
    
    def find(self):
        """
        Find a customer by their username.

        Returns:
        dict: Dictionary representing the customer document in the database.
        """
        customers_collection = self.db.customers
        user = customers_collection.find_one({"username": self.username})
        return user
    
    def find_customer_id_by_username(self, username):
        """
        Find a customer's ID by their username.

        Parameters:
        - username (str): Username of the customer.

        Returns:
        str: Customer ID.
        """
        customers_collection = self.db.customers
        customer = customers_collection.find_one({"username": username})

        if customer:
            return customer["customerId"]
        else:
            return None


