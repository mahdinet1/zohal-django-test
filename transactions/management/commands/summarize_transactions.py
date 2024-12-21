from datetime import datetime

from django.core.management import BaseCommand

from transactions.models import SummaryTransaction
from transactions.repository.transction import TransactionRepository
from transactions.service.transaction_service import TransactionService
import itertools

class Command(BaseCommand):
    help = "Aggregate transactions and store summaries in the summary_transaction collection."

    def handle(self, *args, **kwargs):
        TransactionSvc = TransactionService(repository=TransactionRepository())
        report_types = ['count','amount']
        modes = ['daily','weekly','monthly']
        combinations = list(itertools.product(report_types, modes))
        for  report_type,mode in combinations:
            report = TransactionSvc.get_transaction_report(report_type=report_type, mode=mode)
            report_list = list(report)
            SummaryTransaction.objects(
                merchantId=None,
                type=report_type,
                mode=mode
            ).modify(
                upsert=True,
                new=True,
                set__merchantId=None,
                set__type=report_type,
                set__mode=mode,
                set__report=report_list,
                set__updated_at=datetime.utcnow()
            )

        self.stdout.write("Transaction summaries updated successfully.")

