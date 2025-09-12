from sqlalchemy import insert, select, join
from web.dao.base import BaseDAO
from web.courses.models import CourseModel, CourseTeacherModel
from web.database import async_session_maker
from web.exceptions import CourseNotFoundedException, UserNotFoundedException
from web.users.models import UserModel


class CourseDAO(BaseDAO):
    """DAO для класса 'Курс'
    
    """
    model = CourseModel
    
class CourseTeacherDAO(BaseDAO):
    """DAO для класса 'КурсПреподаватель'
    
    """
    model = CourseTeacherModel
    
    @classmethod
    async def add_teacher(cls, course_id: int, teacher_id: int):
        async with async_session_maker() as session:
            course_query = select(CourseModel).filter_by(id=course_id)
            course_query_res = await session.execute(course_query)
            if not course_query_res.scalar_one_or_none(): 
                raise CourseNotFoundedException
            
            user_query = select(UserModel).filter_by(id=teacher_id)
            user_query_res = await session.execute(user_query)
            if not user_query_res.scalar_one_or_none(): 
                raise UserNotFoundedException    
                    
            query = insert(cls.model).values(course_id=course_id, user_id=teacher_id)
            await session.execute(query)
            await session.commit()
            
            
    @classmethod
    async def get_courses_by_teacher(cls, teacher_id: int):
        """Возвращает все курсы, которые ведет преподаватель

        """
        async with async_session_maker() as session:
            # select u.id as user_id , ct.course_id ,u."name", u.surname , c."name" ,c.description  from "user" u 
            # join course_teachers ct on u.id = ct.user_id 
            # join course c on c.id = ct.course_id
            # where u.id = {user_id}

            sel1 = join(UserModel, CourseTeacherModel, \
                (UserModel.id==CourseTeacherModel.user_id) & (UserModel.id == teacher_id))
            sel2 = join(sel1, CourseModel, \
                (CourseTeacherModel.course_id==CourseModel.id))
            final = select(UserModel.id.label("teacher_id"),
                         UserModel.name.label("teacher_name"),
                         UserModel.surname.label("teacher_surname"),
                         CourseModel.id.label("course_id"),
                         CourseModel.name.label("course_name"),
                         CourseModel.duration.label("course_duration")).select_from(sel2)

            result = await session.execute(final)
            return result.mappings().all()
            
