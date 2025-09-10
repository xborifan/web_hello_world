from datetime import datetime, timedelta
from passlib.context import CryptContext
from pydantic import EmailStr
from jose import jwt

from web.config import settings
from web.users.dao import UserDAO
from web.exceptions import IncorrectEmailOrPassException


pwd_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")

def get_pass_hash(password: str) -> str:
    """Возвращает хэш пароля
    
    """
    return pwd_context.hash(password)

def verify_pass(password: str, hash: str)-> bool:
    """Выполняет сравнивание пароля с хэшем
    
    """    
    return pwd_context.verify(password, hash)

async def auth_user(email: EmailStr, password: str):
    """Выполняет попытку аутентифицировать пользователя по email и паролю
    
    """    
    user = await UserDAO.find_by(email=email)
    if not (user and verify_pass(password, user.password)):
        raise IncorrectEmailOrPassException
    return user

def create_token(data: dict) -> str:
    """Создает JWT-токен
    
    """    
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             settings.JWT_SECRET_KEY,
                             settings.JWT_SECRET_ALG)
    return encoded_jwt
