from fastapi import Depends, Request
from jose import jwt, JWTError

from web.config import settings
from web.exceptions import MissingTokenException, IncorrectTokenException
from web.users.dao import UserDAO

def get_token(req: Request):
    """Возвращает токен пользователя из кукисов
    
    """ 
    token = req.cookies.get("access_token")
    if not token:
        raise MissingTokenException
    return token

async def get_current_user(token: str = Depends(get_token)):
    """Возвращает текущего пользователя на основе токена
    
    """    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            settings.JWT_SECRET_ALG
        )
    except JWTError:
        raise IncorrectTokenException
    
    user_id: int = int(payload.get("sub")) 
    user = await UserDAO.find_by_id(user_id)
    return user