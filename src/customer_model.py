import mongoengine as me


class Address(me.EmbeddedDocument):
    street = me.StringField(required=True)
    city = me.StringField(required=True)
    number = me.StringField(required=True)
    zipCode = me.StringField(required=True)


class PhoneNumber(me.EmbeddedDocument):
    number = me.StringField(required=True)
    type = me.StringField(required=True)


class Customer(me.Document):
    givenName = me.StringField(required=True)
    surName = me.StringField(required=True)
    email = me.StringField(required=True, unique=True)
    afm = me.StringField(required=True, unique=True)
    phoneNumbers = me.ListField(me.EmbeddedDocumentField(PhoneNumber))
    address = me.EmbeddedDocumentField(Address)
    meta = {"collection": "customers", "db_alias": "coding-factory"}
