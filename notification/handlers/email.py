import time

class EmailHandler:
    def send(self, email_addr, message) -> bool:
        """
        Mock implementation of sending an email.
        """
        time.sleep(10)
        raise ValueError("EMAIL service unavailable!")
        print(f"Sending Email to {email_addr}: {message}")
        return True  # Return True if sending succeeds
