from web.dao.base import BaseDAO
from web.users.models import UserModel


class UserDAO(BaseDAO):
    """Класс DAO для класса 'Пользователь'
    
    """
    model = UserModel