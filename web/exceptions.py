from fastapi import HTTPException, status


class BaseException(HTTPException):
    """Базовый класс исключения
    
    """
    status_code = 500
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code,
                         detail=self.detail)


class UserExistException(BaseException):
    """Пользователь уже есть
    
    """    
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь с таким email или логином уже зарегистрирован"

    
class IncorrectEmailOrPassException(BaseException):
    """Пользователь не прошел auth
    
    """    
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Некорректный email или пароль"

    
class MissingTokenException(BaseException):
    """Пользователь не прошел auth
    
    """    
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"

    
class IncorrectTokenException(BaseException):
    """Плохой токен
    
    """    
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Плохой токен"
    
class CourseNotFoundedException(BaseException):
    """Нет такого курса
    
    """    
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Нет такого курса"    
    
class UserNotFoundedException(BaseException):
    """Нет такого пользователя
    
    """    
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Нет такого пользователя"    