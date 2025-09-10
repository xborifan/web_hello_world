from web.dao.base import BaseDAO
from web.courses.models import CourseModel


class CourseDAO(BaseDAO):
    model = CourseModel