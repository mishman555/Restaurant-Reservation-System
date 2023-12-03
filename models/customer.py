class Customer:
    def __init__(self, customerId,username,name,address,phoneNumber,email, seated=False):
        self.customerId=customerId
        self.username=username
        self.name=name
        self.address=address
        self.phoneNumber=phoneNumber
        self.email=email
        self.seated = seated

    def to_dict(self):
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
        return Customer(
            customer_id=data.get("customerId"),
            username=data.get("username"),
            name=data.get("name"),
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            address=data.get("address"),
            seated = data.get("seated")
        )