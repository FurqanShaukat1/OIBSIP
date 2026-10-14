from assistant.email_service import EmailService


email_service = EmailService()

result = email_service.send_email(
    recipient="furqanshaukat12145@gmail.com",
    subject="Voice Assistant Test",
    body="This is a test email sent by my Python voice assistant."
)

print(result)