import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


class EmailService:

    def __init__(self):
        self.smtp_server = os.getenv("EMAIL_SMTP_SERVER")
        self.smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
        self.email = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")

    def send_email(self, recipient, subject, body):

        if not self.smtp_server or not self.email or not self.password:
            return "Email service is not configured."

        if not recipient:
            return "I need a recipient email address."

        if not subject:
            return "I need an email subject."

        if not body:
            return "I need an email message."

        message = EmailMessage()

        message["From"] = self.email
        message["To"] = recipient
        message["Subject"] = subject

        message.set_content(body)

        try:
            with smtplib.SMTP(
                self.smtp_server,
                self.smtp_port,
                timeout=10
            ) as server:

                server.starttls()

                server.login(
                    self.email,
                    self.password
                )

                server.send_message(message)

            return f"Email sent successfully to {recipient}."

        except smtplib.SMTPAuthenticationError:
            return "Email authentication failed. Please check your credentials."

        except smtplib.SMTPException:
            return "I couldn't send the email."

        except OSError:
            return "I couldn't connect to the email server."