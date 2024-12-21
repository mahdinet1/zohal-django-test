from mongoengine import Document, StringField, DateTimeField, FloatField, ObjectIdField, DictField, IntField, ListField


# Create your models here.

class Transaction(Document):
    merchantId = ObjectIdField(required=True)
    amount = FloatField(required=True)
    createdAt = DateTimeField(required=True)


class SummaryTransaction(Document):
    merchantId = StringField(required=False)
    report = ListField(DictField(), required=False, default=[])
    type = StringField(required=True)
    mode = StringField(required=True)
    updated_at = DateTimeField()
