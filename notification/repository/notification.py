from notification.models import Notification


class Repository:

    @staticmethod
    def get_notification_by_id(notification_id):
        return Notification.objects.filter(id=notification_id).first()
