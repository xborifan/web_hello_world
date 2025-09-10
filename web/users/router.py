from fastapi import APIRouter, Depends, Query, Response
from typing import List, Sequence, Any 
from typing_extensions import Annotated

from auth.scheme import get_bearer_token
from web.users.dependencies import get_current_user
from web.users.schemas import UserSchema, UserLoginSchema, UserRegSchema, UserSearchSchema
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

@router.get("")
#async def get_all_users(filter_q: Annotated[UserSearch, Query()]) -> Sequence[User] | User:
async def get_all_users(filter_q: Annotated[UserSearchSchema, Query()], token = Depends(get_bearer_token)) -> Sequence[UserSchema] | UserSchema:
    """Получить информацию обо всех пользователях
    
    """
    filtered = filter_q.model_dump(exclude_unset=True, exclude_defaults=True)
    if filtered:
        return await UserDAO.find_all(**filtered)
    else:
        return await UserDAO.find_all() 

@router.post("/register", status_code=201)
async def register_user(user_data: UserRegSchema):
    """Создать нового пользователя
    
    """
    existing_user = await UserDAO.find_by(email=user_data.email)
    if existing_user is None:
        existing_user = await UserDAO.find_by(login=user_data.login)
        
    if existing_user:
        raise UserExistException
    user_data.password = get_pass_hash(user_data.password)
    await UserDAO.add(**user_data.model_dump())
    return user_data
    

@router.post("/login", status_code=200)
async def login_user(response: Response, user_data: UserLoginSchema):
    """Аутентифицирует пользователя
    
    """
    user = await auth_user(user_data.email, user_data.password)
    accessToken = create_token({"sub": str(user.id)})
    response.set_cookie("access_token", accessToken)
    print(accessToken)
    return user

@router.get("/me", status_code=200)
async def get_me(current_user: UserSchema = Depends(get_current_user)) -> UserSchema:
    """Возвращает текущего пользователя в случае успешной аутентификации 
    
    """
    return current_user
    
@router.get("/{id}")
async def get_user_info(id: int) -> UserSchema:
    """Получить информацию о пользователе
    
    """
    return await UserDAO.find_by_id(id)    