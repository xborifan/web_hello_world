from typing import Optional
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from web.config import settings
from web.exceptions import MissingTokenException


known_tokens = {
    settings.TOKEN_BEARER,
    }
token = HTTPBearer(auto_error=False)

async def get_bearer_token(auth: Optional[HTTPAuthorizationCredentials] = Depends(token)) -> str:
    if auth is None or (token := auth.credentials) not in known_tokens:
        raise MissingTokenException
    return token 