from celery.bin.control import status
from rest_framework.response import Response
from rest_framework.views import APIView
from notification.task import process_notification
from rest_framework import status


# Create your views here.
class NotificationView(APIView):

    def __init__(self):
        super().__init__()

    def post(self, request):
        notification_id = request.data.get("notification_id")
        if not notification_id:
            return Response({"error": "notification_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Add the notification to the Celery queue
            process_notification.delay(notification_id)
            return Response({"message": f"Notification {notification_id} added to the queue."},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error": f"Failed to queue notification: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
