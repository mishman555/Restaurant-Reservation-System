from views.customer import customerView
from views.reservation import reservationView
from views.admin import adminView

class ViewFactory:
    @staticmethod
    def create_customer_view(*args, **kwargs):
        return customerView(*args, **kwargs)

    @staticmethod
    def create_reservation_view(*args, **kwargs):
        return reservationView(*args, **kwargs)

    @staticmethod
    def create_admin_view():
        return adminView()
