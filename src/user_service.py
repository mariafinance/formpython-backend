from src.user_dao import UserDAO
from src.user_dto import UserDTO
from src.user_model import User
from werkzeug.security import check_password_hash


class UserService:
    def __init__(self):
        self.user_dao = UserDAO()

    def register_user(self, user_data):
        user_dto = UserDTO(**user_data)  # Δημιουργία ενός UserDTO από τα δεδομένα
        user = User(
            givenName=user_dto.given_name,  # Αντιστοίχιση από το UserDTO στο User
            surName=user_dto.sur_name,
            email=user_dto.email,
            password=user_dto.password
        )
        self.user_dao.save_user(user)  # Αποθήκευση του User στη βάση δεδομένων
        return user
    
    def check_duplicate_email(self, email):
        return self.user_dao.check_email_exists(email)

    def authenticate_user(self, email, password):
        user = self.user_dao.find_user_by_email(email)
        if user and check_password_hash(user.password, password):
            fullname = f"{user.givenName} {user.surName}"
            identity = {"fullname": fullname, "email": user.email}
            return identity
        return None