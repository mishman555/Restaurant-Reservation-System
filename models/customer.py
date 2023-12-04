class Customer:
    """Class representing a customer in the restaurant reservation system."""
    def __init__(self, customerId,username,name,address,phoneNumber,email, seated=False):
        """
        Initialize a new Customer instance.

        Parameters:
        - customerId (int): The unique identifier for the customer.
        - username (str): The username of the customer.
        - name (str): The name of the customer.
        - address (str): The address of the customer.
        - phoneNumber (str): The phone number of the customer.
        - email (str): The email address of the customer.
        - seated (bool, optional): The seating status of the customer. Defaults to False.
        """
        self.customerId=customerId
        self.username=username
        self.name=name
        self.address=address
        self.phoneNumber=phoneNumber
        self.email=email
        self.seated = seated

    def to_dict(self):
        """
        Convert the Customer instance to a dictionary.
        Returns:
        dict: A dictionary representation of the Customer instance.
        """
        return {
            "customerId": self.customerId,
            "username":self.username,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phoneNumber,
            "address":self.address,
            "seated": self.seated
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Customer instance from a dictionary.

        Parameters:
        - data (dict): A dictionary containing customer data.

        Returns:
        Customer: An instance of the Customer class.
        """
        return Customer(
            customer_id=data.get("customerId"),
            username=data.get("username"),
            name=data.get("name"),
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            address=data.get("address"),
            seated = data.get("seated")
        )