from datetime import datetime, timedelta

from bson import ObjectId

from transactions.models import Transaction, SummaryTransaction


class TransactionRepository:

    @staticmethod
    def get_transactions():
        return Transaction.objects.all()

    @staticmethod
    def add_transaction(transaction_data):
        transaction_data.save()
        return transaction_data

    @staticmethod
    def get_cached_report(report_type, mode, merchant_id=None):
        query = SummaryTransaction.objects(
            mode=mode,
            type=report_type
        )

        if merchant_id:
            query = query.filter(merchantId=merchant_id)


        return query.first().report

    @staticmethod
    def get_all_merchants_reports():
        start_of_day = datetime.strptime("2023-06-10", "%Y-%m-%d")
        # start_of_day = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        # Define the aggregation pipeline
        pipeline = [
            {
                "$match": {  # Match transactions for today
                    "createdAt": {"$gte": start_of_day, "$lt": end_of_day}
                }
            },
            {
                "$group": {  # Group by merchantId
                    "_id": "$merchantId",
                    "total_amount": {"$sum": "$amount"},  # Sum the amount field
                    "transaction_count": {"$count": {}}  # Count the number of transactions
                }
            },
            {
                "$project": {  # Format the output
                    "merchantId": "$_id",
                    "_id": 0,  # Exclude the internal _id field
                    "total_amount": 1,
                    "transaction_count": 1
                }
            }
        ]

        # Execute the aggregation pipeline on the Transaction collection
        reports = Transaction.objects.aggregate(*pipeline)
        return reports

    @staticmethod
    def get_transaction_report(report_type, mode, merchant_id=None):
        match_stage = {"merchantId": ObjectId(merchant_id)} if merchant_id else {}

        if mode == 'daily':
            group_key = {"$dateToString": {"format": "%Y/%m/%d", "date": "$createdAt"}}
        elif mode == 'weekly':
            group_key = {"$concat": [
                "Week ",
                {"$toString": {"$week": "$createdAt"}},
                " of ",
                {"$toString": {"$year": "$createdAt"}}
            ]}
        elif mode == 'monthly':
            group_key = {"$concat": [
                {"$dateToString": {"format": "%B", "date": "$createdAt"}},
                " ",
                {"$toString": {"$year": "$createdAt"}}
            ]}
        else:
            raise ValueError("Invalid mode. Use 'daily', 'weekly', or 'monthly'.")

        accumulator = {"$sum": 1} if report_type == 'count' else {"$sum": "$amount"}

        pipeline = [
            {"$match": match_stage},
            {"$group": {"_id": group_key, "value": accumulator}},
            {"$project": {"key": "$_id", "value": 1}},
            {"$sort": {"key": 1}}
        ]
        transactions = Transaction.objects.aggregate(pipeline)
        return transactions
