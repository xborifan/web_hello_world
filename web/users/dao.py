from web.dao.base import BaseDAO
from web.users.models import User


class UserDAO(BaseDAO):
    model = User