from datetime import datetime
from fastapi import APIRouter
from web.users.schemas import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/{id}")
def get_user_info(id: int) -> User:
    user_data = User(
        name=f"Borifan_{id}",
        surname=f"Ivanov_{id}",
        patronymic=None,
        login=f"ivanov_{id}",
        date_reg=datetime(2024,9,8,14,55),
        date_birth=datetime(1980,5,5,5,5),
        email="admin@ya.ru",
        phone="+78989574123"
        )
    #return "hi"
    #return {"user_id": id, "user_name": "boris"}
    return user_data


@router.post("/")
def register_user(user_data: User) -> User:
    print(f"User saved into DB: {user_data}")
    return user_data
