import datetime
import threading
import time
from datetime import  datetime

from Email import send_email


class EmailTimer:
    def __init__(self, action_method):
        self.action_method = action_method

    def run(self):
        while True:
            now = datetime.now()
            
            # Check if it's midnight (00:00)
            if now.hour == 0 and now.minute == 0:
                print("Email Sending now")
                self.action_method()
                time.sleep(70)  # Sleep for a bit more than a minute to avoid duplicate sends
            else:
                time.sleep(30)  # Sleep for 30 seconds before checking again

email_timer = EmailTimer(send_email)

# Start the timer in a separate thread
timer_thread = threading.Thread(target=email_timer.run)
timer_thread.start()

print("Timer Started")