from src.customer_dao import CustomerDao
from src.customer_dto import CustomerDTO
from src.customer_model import Customer, Address, PhoneNumber
from werkzeug.security import check_password_hash


class CustomerService:
    def __init__(self):
        self.customer_dao = CustomerDao()

    def create_customer(self, customer_data):
        customer_dto = CustomerDTO(**customer_data) #Δημιουργεί ένα CustomerDTO από τα δεδομένα που δίνει ο χρήστης.
        customer = Customer(
            # Αντιστοίχιση από το CustomerDTO στον Customer
            givenName=customer_dto.given_name,
            surName = customer_dto.sur_name,
            email = customer_dto.email,
            afm = customer_dto.afm,
            phoneNumbers = customer_dto.phonenumbers,
            address=customer_dto.address
        )
        self.customer_dao.save_customer(customer) # Αποθήκευση του Customer στη βάση δεδομένων
        return customer
    
    def get_customer_by_email(self, email):
        return self.customer_dao.check_email_exists(email)
    
