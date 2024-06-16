from src.customer_model import Customer

class CustomerDao:
    def save_customer(self, customer):
        try:
            customer.save()
        except Exception as e:
            print(f"Error saving customer : {e}")
            raise e

    # Άλλες μεθόδους ανάκτησης ή ενημέρωσης δεδομένων
    # Αυτή η μέθοδος αναζητά έναν πελάτη στη βάση δεδομένων με βάση το email του.
    def find_customer_by_email(self, email):
        try:
            return Customer.objects(email=email).first()
        except Exception as e:
            print(f"Error finding user by email: {e}")
            raise e
        
    # Αυτή η μέθοδος ελέγχει αν υπάρχει ήδη ένας χρήστης με το συγκεκριμένο email στη βάση δεδομένων.
    def check_email_exists(self, email):
        try:
            return Customer.objects(email=email).count() > 0
        except Exception as e:
            print(f"Error checking if email exists: {e}")
            raise e