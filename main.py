import asyncio
import email
import aiosmtpd.controller
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import AuthResult, LoginPassword, SMTP
# from aiosmtpd.handlers import AuthMixin
# from PIL import Image
# import requests

USERNAME = 'user'         # Replace with your desired username
PASSWORD = 'password123'  # Replace with your desired password
SMTP_HOST = '0.0.0.0'     # Replace with your SMTP server host
SMTP_PORT = 8025            # Replace with your SMTP server port
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


class CustomSMTP(SMTP):
    async def session(self, *args, **kwargs):
        print(f"Client connected: {self.session.peer}")
        await super().session(*args, **kwargs)

    async def push(self, msg):
        print(f"Server: {msg.strip()}")  # Log outgoing server messages
        await super().push(msg)

    async def smtp_HELO(self, *args):
        print(f"Client: HELO {args[0].strip()}")  # Log incoming client message for HELO command
        await super().smtp_HELO(*args)

    async def smtp_EHLO(self, *args):
        print(f"Client: EHLO {args[0].strip()}")  # Log incoming client message for EHLO command
        await super().smtp_EHLO(*args)

    async def smtp_NOOP(self, *args):
        print(f"Client: NOOP {args[0].strip()}")  # Log incoming client message for NOOP command
        await super().smtp_NOOP(*args)

    async def smtp_QUIT(self, *args):
        print("Client: QUIT")  # Log incoming client message for QUIT command
        await super().smtp_QUIT(*args)

    async def smtp_MAIL(self, *args):
        print(f"Client: MAIL {args[0].strip()}")  # Log incoming client message for MAIL command
        await super().smtp_MAIL(*args)

    async def smtp_RCPT(self, *args):
        print(f"Client: RCPT {args[0].strip()}")  # Log incoming client message for RCPT command
        await super().smtp_RCPT(*args)

    async def smtp_DATA(self, *args):
        print(f"Client: DATA {args[0].strip()}")  # Log incoming client message for DATA command
        await super().smtp_DATA(*args)

    async def smtp_RSET(self, *args):
        print(f"Client: RSET {args[0].strip()}")  # Log incoming client message for RSET command
        await super().smtp_RSET(*args)

    async def smtp_VRFY(self, *args):
        print(f"Client: VRFY {args[0].strip()}")  # Log incoming client message for VRFY command
        await super().smtp_VRFY(*args)

    async def smtp_EXPN(self, *args):
        print(f"Client: EXPN {args[0].strip()}")  # Log incoming client message for EXPN command
        await super().smtp_EXPN(*args)

    async def smtp_HELP(self, *args):
        print(f"Client: HELP {args[0].strip()}")  # Log incoming client message for HELP command
        await super().smtp_HELP(*args)

    async def smtp_AUTH(self, *args):
        print(f"Client: AUTH {args[0].strip()}")  # Log incoming client message for AUTH command
        await super().smtp_AUTH(*args)

    async def smtp_STARTTLS(self, *args):
        print(f"Client: STARTTLS {args[0].strip()}")  # Log incoming client message for STARTTLS command
        await super().smtp_STARTTLS(*args)

    async def smtp_UNKNOWN(self, *args):
        print(f"Client: UNKNOWN {args[0].strip()}")  # Log incoming client message for unknown command
        await super().smtp_UNKNOWN(*args)


class CustomController(Controller):
    def factory(self):
        return CustomSMTP(self.handler)


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
    controller = CustomController(
        handler,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        auth_require_tls=False,
        authenticator=authenticator_func,
        factory=CustomSMTP,
    )
    controller.start()
    print("Controller started.")

    while True:
        print("Handling incoming mail...")
        await asyncio.sleep(3600)  # Keep the server running
        print("...sleeping for 60 seconds")


if __name__ == '__main__':
    asyncio.run(main())
