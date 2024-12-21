from django.apps import AppConfig
import mongoengine

MONGODB_SETTINGS = {
    "db": "zibal_db",
    "host": "localhost",
    "port": 27017,
    "username": "admin",
    "password": "admin",
}


class TransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions'

    def ready(self):
        try:
            mongoengine.connect(db=MONGODB_SETTINGS['db'], host=MONGODB_SETTINGS['host'],
                                username=MONGODB_SETTINGS['username'], password=MONGODB_SETTINGS['password'], )
            print("mongo engine connected")

        except Exception as e:
            print("mongoengine connection failed", e)
            exit(1)
