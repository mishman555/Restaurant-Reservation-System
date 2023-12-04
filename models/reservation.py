class Reservation:
    """Class representing a reservation in the restaurant reservation system."""
    def __init__(self, customerId, reservationId, number_of_seats, reservation_date, seated=False, canceled=False):
        """
        Initialize a Reservation instance.

        Parameters:
        - customerId (int): The ID of the customer making the reservation.
        - reservationId (int): The ID of the reservation.
        - number_of_seats (int): The number of seats for the reservation.
        - reservation_date (str): The date and time of the reservation.
        - seated (bool): Flag indicating if the customer has been seated.
        - canceled (bool): Flag indicating if the reservation has been canceled.
        """
        self.customerId = customerId
        self.reservationId = reservationId
        self.number_of_seats = number_of_seats
        self.reservation_date = reservation_date
        self.seated = seated
        self.canceled = canceled

    def to_dict(self):
        """
        Convert the Reservation instance to a dictionary.

        Returns:
        dict: A dictionary representation of the Reservation instance.
        """
        return {
            "customerId": self.customerId,
            "reservationId": self.reservationId,
            "number_of_seats": self.number_of_seats,
            "reservation_date": self.reservation_date,
            "seated": self.seated,
            "canceled": self.canceled
        }
