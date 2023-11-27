import datetime
import time
import threading
import Email as email

class EmailTimer:
      #Made by Chris Athanasi
    def __init__(self, action_method):
        self.action_method = action_method

    def run(self):
        while True:
            now = datetime.datetime.now()
            if now.hour == 12 and now.minute == 9 and current_date.weekday() == 4:
                self.action_method()
                time.sleep(70)  
            else:
                time.sleep(30)

def send_email():
    print("Email sending logic goes here")
    
    email.send_email()

email_timer = EmailTimer(send_email)

# Start the timer in a separate thread
timer_thread = threading.Thread(target=email_timer.run)
timer_thread.start()
current_date = datetime.date.today()

if current_date.weekday() == 4:
    print("Today is Friday!")

print("Timer Start")
