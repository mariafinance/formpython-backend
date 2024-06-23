from src.customer_model import Address, Customer, PhoneNumber

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
        
     #Update Customer function 
    def update_customer(customer_id, update_data):
        try:
            customer = Customer.objects(id=customer_id).first()
            if customer:
                customer.givenName = update_data.get('givenName', customer.givenName)
                customer.surName = update_data.get('surName', customer.surName)
                customer.email = update_data.get('email', customer.email)
                customer.afm = update_data.get('afm', customer.afm)

                # Update phoneNumbers if provided
                if 'phoneNumbers' in update_data:
                    phone_numbers = []
                    for phone in update_data['phoneNumbers']:
                        phone_numbers.append(PhoneNumber(number=phone.get('number'), type=phone.get('type')))
                    customer.phoneNumbers = phone_numbers

                # Update address if provided
                if 'address' in update_data:
                    customer.address = Address(
                        street=update_data['address'].get('street', ''),
                        city=update_data['address'].get('city', ''),
                        number=update_data['address'].get('number', ''),
                        zipCode=update_data['address'].get('zipCode', ''),
                    )

                customer.save()
                return customer
            return None  # Customer not found
        except Exception as e:
            print(f"Error updating customer: {e}")
            return None    