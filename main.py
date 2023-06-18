import asyncio
import email
import aiosmtpd.controller
from aiosmtpd.smtp import AuthResult, LoginPassword
# from aiosmtpd.handlers import AuthMixin
# from PIL import Image
# import requests

USERNAME = 'user'         # Replace with your desired username
PASSWORD = 'password123'  # Replace with your desired password
SMTP_HOST = '0.0.0.0'     # Replace with your SMTP server host
SMTP_PORT = 25            # Replace with your SMTP server port
PUSHOVER_API_TOKEN = 'YOUR_PUSHOVER_API_TOKEN'  # Replace with your Pushover API token
PUSHOVER_USER_KEY = 'YOUR_PUSHOVER_USER_KEY'  # Replace with your Pushover user key


def authenticator_func(server, session, envelope, mechanism, auth_data):
    # For this simple example, we'll ignore other parameters
    print("Authenticating...")
    assert isinstance(auth_data, LoginPassword)
    username = auth_data.login.decode()
    password = auth_data.password.decode()
    print(f"Username: {username}")
    print(f"Password: {password}")
    # if username == USERNAME and password == PASSWORD:
    if True:
        print("Success")
        return AuthResult(success=True)
    else:
        print("Failed")
        return AuthResult(success=False, handled=False)


class EmailHandler():
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    async def handle_DATA(self, server, session, envelope):
        print("Received email message:")
        print(f"From: {envelope.mail_from}")
        print(f"To: {envelope.rcpt_tos}")
        print(f"Data:\n{envelope.content.decode()}")

        return '250 OK'
        # message = email.message_from_bytes(envelope.content)
        # if message.is_multipart():
        #     for part in message.walk():
        #         if part.get_content_maintype() == 'image':
        #             # image_data = part.get_payload(decode=True)
        #             print("Has image")
        #             # image = Image.open(io.BytesIO(image_data))
        #             # resized_image = image.resize((480, 270))  # Adjust dimensions as needed
        #             # resized_image.save('resized_image.jpg', 'JPEG')

        #             # Send push notification with resized image
        #             # files = {'attachment': open('resized_image.jpg', 'rb')}
        #             # files = image_data
        #             # payload = {
        #             #     'token': PUSHOVER_API_TOKEN,
        #             #     'user': PUSHOVER_USER_KEY,
        #             #     'message': 'Motion detected!',
        #             # }
        #             # response = requests.post('https://api.pushover.net/1/messages.json', data=payload, files=files)
        #             # print(response.json())
        #             # break

        # print("Message body:")
        # print(message.get_payload())

        # return '250 OK'

async def main():
    print("Starting Email Handler...")
    handler = EmailHandler(USERNAME, PASSWORD)
    controller = aiosmtpd.controller.Controller(
        handler,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        auth_require_tls=False,
        authenticator=authenticator_func
    )
    controller.start()
    print("Controller started.")

    while True:
        print("Handling incoming mail...")
        await asyncio.sleep(3600)  # Keep the server running
        print("...sleeping for 60 seconds")


if __name__ == '__main__':
    asyncio.run(main())
