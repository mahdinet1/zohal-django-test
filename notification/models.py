from mongoengine import Document, StringField, ListField, DateTimeField, IntField

# Create your models here.
class Notification(Document):
    message = StringField(required=True)
    recipient = StringField(required=True)  # Can be email, phone number, etc. base on medium
    medium = StringField(required=True)
    task_type = StringField(required=True,default='no-type')
    status = StringField(default="pending")  # pending, sent, failed
    retries = IntField(default=0)
    created_at = DateTimeField()
    updated_at = DateTimeField()
    logs = ListField(StringField())  # Log of retries or errors