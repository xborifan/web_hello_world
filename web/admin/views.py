from sqladmin import ModelView

from web.users.models import UserModel
from web.courses.models import CourseModel


class UsersAdmin(ModelView, model=UserModel):
    can_create = False
    can_delete = True
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = [
        UserModel.id,
        UserModel.name,
        UserModel.surname,
        UserModel.email
                   ]
    column_details_exclude_list = [
        UserModel.password
    ]
    
    
class CoursesAdmin(ModelView, model=CourseModel):
    can_create = False
    can_delete = True
    name = "Курс"
    name_plural = "Курсы"
    column_list = [
        CourseModel.id,
        CourseModel.name,
        CourseModel.description,
        CourseModel.duration,
        CourseModel.teacher_id
                   ]    