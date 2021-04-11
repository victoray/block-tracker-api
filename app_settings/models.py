from typing import Optional

from common.models import Ownable


class Settings(Ownable):
    allowNotifications = True
    email: Optional[str]
