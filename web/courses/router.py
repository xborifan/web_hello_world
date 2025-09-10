from fastapi import APIRouter, Depends, Query, status, Response
from fastapi.responses import JSONResponse
from typing import List, Sequence, Any 
from typing_extensions import Annotated

from auth.scheme import get_bearer_token
from web.users.dependencies import get_current_user, get_token

from web.courses.schemas import CourseRegSchema, CourseSearchSchema, CourseSchema
from web.courses.dao import CourseDAO
from web.exceptions import UserExistException
from web.auth import create_token, get_pass_hash, auth_user


router = APIRouter(
    prefix="/courses",
    tags=["Курсы"]
)

@router.get("")
#async def get_all_users(filter_q: Annotated[UserSearch, Query()]) -> Sequence[User] | User:
async def get_all_courses(filter_q: Annotated[CourseSearchSchema, Query()], token = Depends(get_bearer_token)) -> Sequence[CourseSchema] | CourseSchema:
    """Получить информацию обо всех курсах
    
    """
    print(filter_q)
    filtered = filter_q.model_dump(exclude_unset=True, exclude_defaults=True)
    if filter_q:
        return await CourseDAO.find_all(**filtered)
    else:
        return await CourseDAO.find_all() 
    
@router.get("/{id}")
async def get_course_info(id: int) -> CourseSchema:
    """Получить информацию о пользователе
    
    """
    return await CourseDAO.find_by_id(id)    

@router.post("/add", status_code=201)
async def add_course(course_data: CourseRegSchema):
    """Создать нового пользователя
    
    """
    await CourseDAO.add(**course_data.model_dump())
    
@router.delete("/")
async def del_course(ids: Annotated[List[int], Query(description="Идентификатор(ы) курса")]):
    """Удалить курс
    
    """
    return await CourseDAO.del_by_id(ids)