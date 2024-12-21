
from rest_framework.response import Response
from rest_framework.views import APIView
from transactions.repository.transction import TransactionRepository
from transactions.serializer import AggregationResultSerializer
from transactions.service.transaction_service import TransactionService
from rest_framework import status
import bson

TransactionSvc = TransactionService(repository=TransactionRepository())
class TransactionViewSet(APIView):
    def __init__(self):
        super().__init__()


    def get(self, request):
        mode = request.query_params.get('mode')
        output_type = request.query_params.get('type')
        obj_id = request.query_params.get('merchantId')

        # sanitize query
        # TODO - sanitize it in separate package
        if mode is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "mode is required"})
        if mode not in ['daily', 'weekly', 'monthly']:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"error": "mode is invalid. it should be daily or weekly or monthly"})

        if output_type is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "type is required"})

        if obj_id is not None and not bson.objectid.ObjectId.is_valid(obj_id):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "merchantId is invalid"})

        serializer = AggregationResultSerializer(
            TransactionSvc.get_transaction_report(report_type=output_type, mode=mode, merchant_id=obj_id),
            many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CachedReportView(APIView):
    def get(self, request):

        mode = request.query_params.get('mode')
        output_type = request.query_params.get('type')
        obj_id = request.query_params.get('merchantId')

        # sanitize query
        # TODO - sanitize it in separate package
        if mode is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "mode is required"})
        if mode not in ['daily', 'weekly', 'monthly']:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"error": "mode is invalid. it should be daily or weekly or monthly"})

        if output_type is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "type is required"})

        if obj_id is not None and not bson.objectid.ObjectId.is_valid(obj_id):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "merchantId is invalid"})

        serializer = AggregationResultSerializer(
            TransactionSvc.get_cached_report(report_type=output_type, mode=mode, merchant_id=obj_id),
            many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
