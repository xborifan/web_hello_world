from fastapi import APIRouter, Depends, Query, status, Response
from fastapi.responses import JSONResponse
from typing import List, Sequence, Any 
from typing_extensions import Annotated

from web.users.dependencies import get_current_user, get_token
from web.users.schemas import User, UserLogin, UserReg, UserSearch
from web.users.dao import UserDAO
from web.exceptions import UserExistException
from web.auth import create_token, get_pass_hash, auth_user

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)


@router.delete("/")
async def del_user(ids: Annotated[List[int], Query(description="Идентификатор(ы) пользователя")]):
    """Удалить пользователя
    
    """
    return await UserDAO.del_by_id(ids)

# @router.get("")
# async def get_all_users(name: str="") -> Sequence[User] | User:
#     """Получить информацию обо всех пользователях
    
#     """
#     if name:
#         return await UserDAO.find_all(name=name)
#     else:
#         return await UserDAO.find_all() 



@router.get("")
#async def get_all_users(filter_q: Annotated[UserSearch, Query()]):
async def get_all_users(filter_q: Annotated[UserSearch, Query()]) -> Sequence[User] | User:
    """Получить информацию обо всех пользователях
    
    """
    print(filter_q)
    filtered = filter_q.model_dump(exclude_unset=True, exclude_defaults=True)
    if filter_q:
        return await UserDAO.find_all(**filtered)
    else:
        return await UserDAO.find_all() 

@router.post("/register", status_code=201)
async def register_user(user_data: UserReg):
    """Создать нового пользователя
    
    """
    existing_user = await UserDAO.find_by(email=user_data.email)
    if existing_user:
        raise UserExistException
    user_data.password = get_pass_hash(user_data.password)
    await UserDAO.add(**user_data.model_dump())
    print(f"User saved into DB: {user_data}")
    #return user_data

@router.post("/login", status_code=200)
async def login_user(response: Response, user_data: UserLogin):
    user = await auth_user(user_data.email, user_data.password)
    accessToken = create_token({"sub": str(user.id)})
    response.set_cookie("access_token", accessToken)
    print(accessToken)
    return user

@router.get("/me", status_code=200)
async def get_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
    
@router.get("/{id}")
async def get_user_info(id: int) -> User:
    """Получить информацию о пользователе
    
    """
    return await UserDAO.find_by_id(id)    