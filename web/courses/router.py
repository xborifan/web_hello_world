import json
from fastapi import APIRouter, Depends, Query
from typing import List, Sequence 
from typing_extensions import Annotated

from auth.scheme import get_bearer_token

from web.courses.schemas import CourseRegSchema, CourseSearchSchema, CourseSchema
from web.courses.dao import CourseDAO, CourseTeacherDAO
from web.users.dependencies import get_current_user
from web.users.models import UserModel
from web.users.router import get_me
from web.users.schemas import UserSchema


router = APIRouter(
    prefix="/courses",
    tags=["Курсы"]
)

@router.get("")
#async def get_all_users(filter_q: Annotated[UserSearch, Query()]) -> Sequence[User] | User:
async def get_all_courses(filter_q: Annotated[CourseSearchSchema, Query()], token = Depends(get_bearer_token)) -> Sequence[CourseSchema] | CourseSchema:
    """Получить информацию обо всех курсах
    
    """
    filtered = filter_q.model_dump(exclude_unset=True, exclude_defaults=True)
    if filtered:
        return await CourseDAO.find_all(**filtered)
    else:
        return await CourseDAO.find_all() 


@router.get("/get_my")
async def get_my_courses(user: UserSchema = Depends(get_current_user)):
    """Получить информацию о курсе
    
    """
    return await CourseTeacherDAO.get_courses_by_teacher(user.id)


@router.get("/{id}")
async def get_course_info(id: int) -> CourseSchema:
    """Получить информацию о курсе
    
    """
    return await CourseDAO.find_by_id(id)    

@router.post("/add", status_code=201)
async def add_course(course_data: CourseRegSchema):
    """Добавить новый курс
    
    """
    await CourseDAO.add(**course_data.model_dump())
    
@router.post("/add_teacher", status_code=201)
async def add_teacher_to_course(course_id: int, teacher_id: int):
    """Добавить новый курс
    
    """
    await CourseTeacherDAO.add_teacher(course_id=course_id, teacher_id=teacher_id)
    
@router.delete("/")
async def del_course(ids: Annotated[List[int], Query(description="Идентификатор(ы) курса")]):
    """Удалить курс
    
    """
    return await CourseDAO.del_by_id(ids)
