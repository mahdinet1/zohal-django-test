from pyexpat.errors import messages

from celery import shared_task

from notification.models import Notification
from notification.task import process_notification
from transactions.repository.transction import TransactionRepository
from transactions.service.transaction_service import TransactionService

TransactionSvc = TransactionService(repository=TransactionRepository())


@shared_task
def sending_report():
    reports = TransactionSvc.get_merchants_reports()
    for report in list(reports):
        notif = Notification(
            recipient=str(report['merchantId']),
            message=f'your daily report: total-amount={report["total_amount"]} and transaction count: total-count={report["transaction_count"]}',
            medium='sms',
            task_type='transaction-daily-report',
        )
        notif.save()
        process_notification.delay(str(notif.id))
