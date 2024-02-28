import imaplib
import smtplib
import email
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailNotifier:
    def __init__(self, smtp_server='smtp.gmail.com', imap_server='imap.gmail.com'):
        self.smtp_server = smtp_server
        self.imap_server = imap_server

    def send_email(self, sender_email, sender_password, receiver_email, subject, body):
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(self.smtp_server, 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

    def check_unread_emails(self, email_address, password):
        mail = imaplib.IMAP4_SSL(self.imap_server)
        mail.login(email_address, password)
        mail.select("inbox")
        result, data = mail.search(None, "(UNSEEN)")
        email_ids = data[0].split()

        if email_ids:
            print("You have unread emails.")
        else:
            print("You have no unread emails.")
            

def main():
    smtp_server = 'smtp.gmail.com'
    imap_server = 'imap.gmail.com'

    email_address = "xeroxavishek@gmail.com"
    password = "povx twai tzqy odah"
    receiver_email = "saikot.roy18@gmail.com"
    
    notifier = EmailNotifier(smtp_server, imap_server)

    while True:
        notifier.check_unread_emails(email_address, password)
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
