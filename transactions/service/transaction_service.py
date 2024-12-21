import abc
from enum import Enum

from transactions.models import Transaction


class Mode(Enum):
    daily = 1
    weekly = 2
    monthly = 3


class TransactionType(Enum):
    count = 1
    amount = 2


class Repository:
    @abc.abstractmethod
    def get_transactions(self):
        pass

    @abc.abstractmethod
    def add_transaction(self, transaction):
        pass

    @abc.abstractmethod
    def get_transaction_report(self, report_type, mode, merchant_id=None):
        pass

    @abc.abstractmethod
    def get_all_merchants_reports(self):
        pass

    @abc.abstractmethod
    def get_cached_report(self,report_type, mode, merchant_id=None):
        pass

class TransactionService:
    def __init__(self, repository: Repository):
        self.repository = repository

    # TODO - mode can be enum
    def get_transactions(self):
        return self.repository.get_transactions()

    def add_transaction(self, transaction: Transaction):
        self.repository.add_transaction(transaction)
        return transaction

    def get_transaction_report(self, report_type, mode, merchant_id=None):
        return self.repository.get_transaction_report(report_type, mode, merchant_id)

    def get_merchants_reports(self):
        reports = self.repository.get_all_merchants_reports()
        return reports


    def get_cached_report(self, report_type, mode, merchant_id=None):
        return self.repository.get_cached_report(report_type, mode, merchant_id)