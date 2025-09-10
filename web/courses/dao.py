from web.dao.base import BaseDAO
from web.courses.models import CourseModel


class CourseDAO(BaseDAO):
    """Класс DAO для класса 'Курс'
    
    """
    model = CourseModel