import smtplib
from email.message import EmailMessage


def send_test_email():
    sender = 'sender@test.home.arpa'  # Replace with the sender's email address
    recipient = 'recipient@test.home.arpa'  # Replace with the recipient's email address
    username = 'user'  # Replace with your SMTP server username
    password = 'password123'  # Replace with your SMTP server password
    smtp_server = '127.0.0.1'  # Replace with your SMTP server address
    smtp_port = 25  # Replace with your SMTP server port

    message = EmailMessage()
    message['Subject'] = 'Test Email'
    message['From'] = sender
    message['To'] = recipient
    message.set_content('This is a test email.')

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.send_message(message)
        print("Test email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Error sending the test email: {str(e)}")


if __name__ == '__main__':
    send_test_email()
