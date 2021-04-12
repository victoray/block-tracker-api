import requests

from app_settings.db import settings_collection
from app_settings.models import Settings
from settings import MAILGUN_API_KEY

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
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": from_,
                "to": to,
                "subject": subject,
                "text": text,
            },
        )


def send_email(user_id: str, subject: str, text: str):
    settings = settings_collection.find_one({"userId": user_id})
    if not settings:
        return

    settings = Settings.parse_obj(settings)

    email = settings.email
    if email and settings.allowNotifications:
        client = MailGunClient()
        client.send_email(to=email, subject=subject, text=text)
