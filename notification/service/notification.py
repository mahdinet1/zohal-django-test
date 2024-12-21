import abc
import time
from datetime import datetime
from time import sleep

from notification.models import Notification


class SmsHandler:
    @abc.abstractmethod
    def send(self, phone_number, message) -> bool:
        pass


class EmailHandler:
    @abc.abstractmethod
    def send(self, email_addr, message) -> bool:
        pass


class Repository:
    @abc.abstractmethod
    def get_notification_by_id(self, notification_id) -> Notification:
        pass


# TODO -  status should be sth like enum
class NotificationService:
    def __init__(self, sms_handler: SmsHandler, email_handler: EmailHandler, repository: Repository):
        self.handlers = {
            'sms': sms_handler,
            'email': email_handler
        }
        self.repository = repository

    # TODO - it should have a policy to define a status for each medium and have a retry counter for each medium separately
    def send_notification(self, notification_id):
        notification = self.repository.get_notification_by_id(notification_id)
        if not notification:
            raise ValueError('Notification with id {} not found'.format(notification_id))

        medium = notification.medium
        if medium not in self.handlers:
            raise ValueError('Medium {} is not supported'.format(medium))

        handler = self.handlers.get(medium)
        if not handler:
            notification.status = "failed"
            notification.logs.append(f"Handler for {medium} not found")

        try:
            success = handler.send(notification.recipient, notification.message)
            if success:
                notification.status = "success"
                notification.logs.append(f"Message sent via {medium}")

            else:
                notification.status = "failed"
                notification.logs.append(f"Message failed to send for {medium}")

        except Exception as e:
            notification.status = "failed"
            notification.logs.append(f"error sending via {medium}: {e}")
            notification.retries += 1
            notification.updated_at = datetime.utcnow()
            notification.save()
            raise ValueError(f"Error while sending notification via {medium}: {e}")

        notification.retries += 1
        notification.updated_at = datetime.utcnow()
        notification.save()
