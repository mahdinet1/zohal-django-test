import time


class SmsHandler:
    def send(self, phone_number, message) -> bool:
        """
        Mock implementation of sending an SMS.
        """
        time.sleep(30)
        print(f"Sending SMS to {phone_number}: {message}")
        return True  # Return True if sending succeeds
