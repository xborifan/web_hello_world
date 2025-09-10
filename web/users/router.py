from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from typing import List, Sequence
from typing_extensions import Annotated

from web.users.schemas import User, UserReg
from web.users.dao import UserDAO


router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)

@router.get("/{id}")
async def get_user_info(id: int) -> User:
    """Получить информацию о пользователе
    
    """
    return await UserDAO.find_by_id(id)

@router.delete("/")
async def del_user(ids: Annotated[List[int], Query(description="Идентификатор(ы) пользователя")]):
    """Удалить пользователя
    
    """
    return await UserDAO.del_by_id(ids)

@router.get("")
async def get_all_users() -> Sequence[User]:
    """Получить информацию обо всех пользователях
    
    """
    return await UserDAO.find_all()


@router.post("/register")
async def register_user(user_data: UserReg):
    """Создать нового пользователя
    
    """
    await UserDAO.add(**user_data.model_dump())
    print(f"User saved into DB: {user_data}")
    #return user_data
