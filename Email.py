from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib
import pathlib


recieverEmails = [
    
   'Chrisathanasi859@gmail.com',
  
    
    
    ]




 #The sender email DO NOT EDIT ANY OF THIS!!!!!!!!!!!!!!!!!!!!!!!!!!
emailSender = 'pythonbot562@gmail.com'
emailPassword = 'ldbj bunk mpfp wktc'
#Serisouly it will break do not change anything here lmao

 #A list of recievers that will recive said email

 #Self explainable variables
subject = 'Time card'
body = f"""




 """

em = MIMEMultipart()
em['From'] = emailSender
em['To'] = ','.join(recieverEmails)
em['Subject'] = subject
em.attach(MIMEText(body, 'plain'))

 #Define the file to attach
filename =  'test.txt'
print("We will try and mail the: " + filename)

 #open the file in python as a binary
attachments = open(filename, 'rb')

 #Encode as base 64
attachments_package = MIMEBase('application', 'octet-stream')
attachments_package.set_payload((attachments).read())
encoders.encode_base64(attachments_package)
attachments_package.add_header('Content-Disposition', "attachment; filename = " + filename)
em.attach(attachments_package)
text = em.as_string()




try:

     TIE_server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=120)
     TIE_server.login(emailSender, emailPassword)

     #Send the email to every person in the list 
     for person in recieverEmails:
      TIE_server.sendmail(emailSender, person, text)
    #print("Success logging in email is being sent to: " + ReciverEmail)
     TIE_server.quit()


except smtplib.SMTPException as e:
     print("SMTP error occurred:", e)

