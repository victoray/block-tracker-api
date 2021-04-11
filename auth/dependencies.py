from typing import Optional

import firebase_admin
from fastapi import Header, Security, HTTPException
from firebase_admin import auth

from auth.models import User
from settings import FIREBASE_APP


def get_current_user(Authorization: Optional[str] = Header(None)):
    if Authorization:
        _, token = Authorization.split(" ")
        user = auth.verify_id_token(token, app=firebase_admin.get_app(FIREBASE_APP))
        return User(uid=user.get("uid"))

    raise HTTPException(status_code=403, detail="Invalid authorization header")


async def get_current_active_user(current_user: User = Security(get_current_user)):
    return current_user
