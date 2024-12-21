from rest_framework_mongoengine import serializers
from rest_framework import serializers as sz
from transactions.models import Transaction


class TransactionSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'



class FileUploadSerializer(sz.Serializer):
    file = sz.FileField()


class AggregationResultSerializer(sz.Serializer):
    key = sz.CharField()
    value = sz.DecimalField(max_digits=90, decimal_places=2)