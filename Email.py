from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
from datetime import datetime
from DataManagement.DataController import DataControl

#This method will allow us to add emails from a txt file in our current directory
def get_receiver_emails(filename='receiver_emails.txt'):
   
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write('\n')
    
    with open(filename, 'r') as file:
        return [email.strip() for email in file.readlines()]

def send_email():
    email_sender = 'pythonbot562@gmail.com'
    email_password = 'ldbj bunk mpfp wktc' 

    receiver_emails = get_receiver_emails()  

    current_datetime = datetime.now()
    is_saturday = current_datetime.weekday() == 5 # Weekly time card will be mailed out on SATURDAY at exactly 12:00 AM

    data_control = DataControl()

    if is_saturday:
        subject = 'Weekly Time Card'
        filename = data_control.getFileName()
        data_control.createFile()
        print("Weekly Time Card has been Emailed")
        folder = "Weekly Time Cards"
    else:
        subject = 'Daily Time Card'
        filename = data_control.getDailyFileName()
        data_control.createFile(daily=True)
        folder = "Daily Time Cards"

    full_path = os.path.join(folder, filename)
    body = data_control.getEmailBody(filename, folder) if os.path.exists(full_path) else "File not found."

    em = MIMEMultipart()
    em['From'] = email_sender
    em['To'] = ','.join(receiver_emails)
    em['Subject'] = subject
    em.attach(MIMEText(body, 'plain'))

    if os.path.exists(full_path):
        with open(full_path, 'rb') as attachments:
            attachments_package = MIMEBase('application', 'octet-stream')
            attachments_package.set_payload(attachments.read())
            encoders.encode_base64(attachments_package)
            attachments_package.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(full_path)}")
            em.attach(attachments_package)

    text = em.as_string()

    try:
        TIE_server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=120)
        TIE_server.login(email_sender, email_password)
        for person in receiver_emails:
            TIE_server.sendmail(email_sender, person, text)
        TIE_server.quit()
        print("Email sent successfully.")
    except smtplib.SMTPException as e:
        print("SMTP error occurred:", e)


get_receiver_emails()