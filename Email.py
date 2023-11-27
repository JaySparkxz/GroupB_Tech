from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import ssl
from DataManagement.DataController import DataControl

def send_email():
    # Receiver emails
    receiver_emails = ['']

    # Sender email credentials
    email_sender = 'pythonbot562@gmail.com'
    email_password = 'ldbj bunk mpfp wktc'

    # Email subject
    subject = 'Time card'

    # Create DataControl instance and set the email body with CSV contents
    data_control = DataControl()
    body = data_control.setEmailBody(data_control.getFileName())

    # Create the email
    em = MIMEMultipart()
    em['From'] = email_sender
    em['To'] = ','.join(receiver_emails)
    em['Subject'] = subject
    em.attach(MIMEText(body, 'plain'))

    # Define and attach the file
    filename = data_control.getFileName()
    full_path = os.path.join("TimeCards", filename)  # Correct the file path

    with open(full_path, 'rb') as attachments:  # Use the full path here
        attachments_package = MIMEBase('application', 'octet-stream')
        attachments_package.set_payload(attachments.read())
        encoders.encode_base64(attachments_package)
        attachments_package.add_header('Content-Disposition', f"attachment; filename= {filename}")
        em.attach(attachments_package)
    print("We will try and mail the: " + filename)

    # Convert the email to a string
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


