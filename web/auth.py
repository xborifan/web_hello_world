from datetime import datetime, timedelta
from passlib.context import CryptContext
from pydantic import EmailStr
from jose import jwt

from web.config import settings
from web.users.dao import UserDAO
from web.exceptions import IncorrectEmailOrPassException


pwd_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")

def get_pass_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_pass(password: str, hash: str)-> bool:
    return pwd_context.verify(password, hash)
    

async def auth_user(email: EmailStr, password: str):
    user = await UserDAO.find_by(email=email)
    h = user.password
    if not (user and verify_pass(password, h)):
        raise IncorrectEmailOrPassException
    return user

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,
                             settings.JWT_SECRET_KEY,
                             settings.JWT_SECRET_ALG)
    return encoded_jwt

if __name__=="__main__":
    #print(get_pass_hash("123"))
    pass