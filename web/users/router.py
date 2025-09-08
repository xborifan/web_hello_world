from datetime import datetime
from fastapi import APIRouter
from web.users.schemas import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/{id}")
def get_user_info(id: int) -> User:
    """Получить информацию о пользователе
    
    """
    user_data = User(
        name=f"Borifan_{id}",
        surname=f"Ivanov_{id}",
        patronymic=None,
        login=f"ivanov_{id}",
        dateOfReg=datetime(2024,9,8,14,55),
        dateOfBirth=datetime(1980,12,31),
        email="Admin@ya.ru",
        phone="+79125555555"
        )
    return user_data


@router.post("/")
def register_user(user_data: User) -> User:
    """Создать нового пользователя
    
    """
    print(f"User saved into DB: {user_data}")
    return user_data
