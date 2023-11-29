from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
from datetime import datetime
from DataManagement.DataController import DataControl

def send_email():
    # Receiver emails
    receiver_emails = ['']  # Replace with actual receiver email

    # Sender email credentials
    email_sender = 'pythonbot562@gmail.com'
    email_password = 'ldbj bunk mpfp wktc'  

    # Check the current day and time
    current_datetime = datetime.now()
    is_saturday_midnight = current_datetime.weekday() == 5 and current_datetime.hour == 0


    data_control = DataControl()

    # Set the email subject and body with CSV contents based on the day and time
    if is_saturday_midnight:
        subject = 'Weekly Time Card'
        filename = data_control.getFileName()
        folder = "Weekly Time Cards"
    else:
        subject = 'Daily Time Card'
        filename = data_control.getDailyFileName()
        folder = "Daily Time Cards"

    # Ensure the file path is correct
    full_path = os.path.join(folder, filename)

    body = data_control.getEmailBody(filename, folder) if os.path.exists(full_path) else "File not found."

    # Create the email
    em = MIMEMultipart()
    em['From'] = email_sender
    em['To'] = ','.join(receiver_emails)
    em['Subject'] = subject
    em.attach(MIMEText(body, 'plain'))

    # Define and attach the file
    if os.path.exists(full_path):
        with open(full_path, 'rb') as attachments:
            attachments_package = MIMEBase('application', 'octet-stream')
            attachments_package.set_payload(attachments.read())
            encoders.encode_base64(attachments_package)
            attachments_package.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(full_path)}")
            em.attach(attachments_package)


    text = em.as_string()

    # Send the email
    try:
        TIE_server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=120)
        TIE_server.login(email_sender, email_password)

        # Send the email to every person in the list
        for person in receiver_emails:
            TIE_server.sendmail(email_sender, person, text)
        TIE_server.quit()
        print("Email sent successfully.")

    except smtplib.SMTPException as e:
        print("SMTP error occurred:", e)

# Call the send_email function
send_email()
