import requests

from app_settings.db import settings_collection

DEFAULT_EMAIL = (
    "Block Tracker <postmaster@sandbox38920d794f42405e81f5689097f0cc19.mailgun.org>"
)


class MailGunClient:
    url = "https://api.mailgun.net/v3/sandbox38920d794f42405e81f5689097f0cc19.mailgun.org/messages"

    def send_email(
        self,
        to: str,
        subject: str,
        text: str,
        from_=DEFAULT_EMAIL,
    ):
        return requests.post(
            self.url,
            auth=("api",),
            data={
                "from": from_,
                "to": to,
                "subject": subject,
                "text": text,
            },
        )


def send_email(user_id: str, subject: str, text: str):
    settings: dict = settings_collection.find_one({"userId": user_id})
    if not settings:
        return

    email = settings.get("email")
    if email:
        client = MailGunClient()
        client.send_email(to=email, subject=subject, text=text)
