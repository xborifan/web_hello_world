from pydantic import BaseModel, Field, EmailStr, field_validator as fv
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional, Annotated
from datetime import datetime, date


class RussianPhoneNumber(PhoneNumber):
    """Тип данных для телефонного нормера РФ
    
    """    
    supported_regions = ["RU"]
    default_region_code = "+7"
    

class UserRegSchema(BaseModel):
    """Модель [Pydantic] "Новый пользователь системы"
    
    """
    email:       Annotated[EmailStr,                     Field(description="Адрес электронной почты")]
    login:       Annotated[str,                          Field(description="Логин")]
    dateOfBirth: Annotated[date,                         Field(description="Дата рождения")]
    name:        Annotated[Optional[str],                Field(description="Имя")]
    surname:     Annotated[Optional[str],                Field(description="Фамилия")]    
    patronymic:  Annotated[Optional[str],                Field(description="Отчество")]
    phone:       Annotated[Optional[RussianPhoneNumber], Field(description="Номер телефона для связи")]
    password:    Annotated[str,                          Field(description="Пароль")]
    
    @fv("dateOfBirth")
    def validate_age(cls, value: date):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise ValueError(f"Вам должно быть больше 18 лет! ({age} - это недостаточно)")
        if age > 99:
            raise ValueError(f"Старикам здесь не место! ({age} - это многовато)")
        return value
    
    @fv("login")
    def validate_login(cls, value: str):
        if value.strip() == "":
            raise ValueError(f"Логин не может быть пустым!")
        cls.login = value.strip().lower()
        return value.strip().lower()
    
    @fv("name", "surname", "patronymic")
    def validate_fio(cls, value: str):
        return value.strip().capitalize() if value else value
    
    @fv("email", mode="after")
    def validate_email(cls, value: EmailStr):
        return value.strip().lower() if value else value

    @fv("phone", mode="before")
    def validate_phone(cls, value: str):
        if value:
            value = value.strip()
            if value.startswith("8"):
                value = value.replace("8", "+7", 1)
        return value
    
    
class UserSchema(BaseModel):
    """Модель [Pydantic] "Пользователь системы"

    """
    id:          Annotated[Optional[int],                Field(description="Идентификатор", default=None)]
    name:        Annotated[Optional[str],                Field(description="Имя", default="UserName")]
    surname:     Annotated[Optional[str],                Field(description="Фамилия", default="UserSurName" )]
    login:       Annotated[str,                          Field(description="Логин", default="")]
    dateOfBirth: Annotated[date,                         Field(description="Дата рождения", default=None)]
    dateOfReg:   Annotated[datetime,                     Field(description="Момент регистрации пользователя", default=None)]
    patronymic:  Annotated[Optional[str],                Field(description="Отчество", default="")]
    email:       Annotated[EmailStr,                     Field(description="Адрес электронной почты", default=None)]
    phone:       Annotated[Optional[RussianPhoneNumber], Field(description="Номер телефона для связи", default=None)]
    #password:    Annotated[Optional[str], Field(description="Пароль", default="")]


class UserSearchSchema(BaseModel):
    """Модель [Pydantic] "Пользователь для поиска"
    
    """
    name:        str = ""
    surname:     str = ""
    login:       str = ""
    dateOfBirth: date = None
    dateOfReg:   datetime = None
    patronymic:  str = ""
    email:       str = ""
    phone:       str = ""
    password:    str = ""


class UserLoginSchema(BaseModel):
    """Модель [Pydantic] "Пользователь для логина"
    
    """
    email:        str = ""
    password:     str = ""