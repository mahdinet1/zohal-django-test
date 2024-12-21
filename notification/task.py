from celery import shared_task
from notification.service.notification import NotificationService
from notification.handlers.sms import SmsHandler
from notification.handlers.email import EmailHandler
from notification.repository.notification import Repository


@shared_task(bind=True,max_retries=3, default_retry_delay=60)
def process_notification(self,notification_id):
    sms_handler = SmsHandler()
    email_handler = EmailHandler()
    repository = Repository()

    service = NotificationService(sms_handler, email_handler, repository)

    try:
        service.send_notification(notification_id)
        print(f"Notification {notification_id} processed successfully.")
    except Exception as e:
        print(f"Failed to process notification {notification_id}: {e}")
        self.retry(exc=e)

