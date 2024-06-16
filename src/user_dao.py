from src.user_model import User

class UserDAO:
    def save_user(self, user):
        try:
            user.save()
        except Exception as e:
            print(f"Error saving user: {e}")
            raise e

    # Άλλες μεθόδους ανάκτησης ή ενημέρωσης δεδομένων
    # Αυτή η μέθοδος αναζητά έναν χρήστη στη βάση δεδομένων με βάση το email του.
    def find_user_by_email(self, email):
        try:
            return User.objects(email=email).first()
        except Exception as e:
            print(f"Error finding user by email: {e}")
            raise e
        
    # Αυτή η μέθοδος ελέγχει αν υπάρχει ήδη ένας χρήστης με το συγκεκριμένο email στη βάση δεδομένων.
    def check_email_exists(self, email):
        try:
            return User.objects(email=email).count() > 0
        except Exception as e:
            print(f"Error checking if email exists: {e}")
            raise e

