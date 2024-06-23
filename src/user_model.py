import mongoengine as me
from werkzeug.security import generate_password_hash


class User(me.Document):
    givenName = me.StringField(required=True)
    surName = me.StringField(required=True)
    email = me.StringField(required=True, unique=True)
    password = me.StringField(required=True)
    meta = {"collection": "users", "db_alias": "coding-factory"}
    role = me.StringField(required=True, default='user') # default role is 'user'

    def save(self, *args, **kwargs):
        self.password = generate_password_hash(self.password)
        super(User, self).save(*args, **kwargs)

##In my service, check user roles Note: to be fixed as per layer arch
def has_role(user, role):
    return user.role == role

