import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'anjanawickramasinghe7@gmail.com'
SENDER_PASSWORD = 'drfs wkbg josy pwdb'

def send_email(to_email, subject, body):
    try:
        print(f"Attempting to send email from {SENDER_EMAIL} to {to_email}")
        
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.set_debuglevel(1)  # Shows detailed SMTP communication
        
        print("Starting TLS...")
        server.starttls()
        
        print("Logging in...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        print("Sending message...")
        server.send_message(message)
        
        print("Closing connection...")
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication failed: {e}")
        return False
    except Exception as error:
        print(f"Error sending email: {error}")
        return False