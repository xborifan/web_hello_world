from pydantic import BaseModel, Field, EmailStr, field_validator as fv
from typing import Optional, Annotated
from datetime import datetime, date


class CourseRegSchema(BaseModel):
    """Модель [Pydantic] "Новый пользователь системы"
    
    """
    name:        Annotated[str,           Field(description="Имя")]
    description: Annotated[Optional[str], Field(description="Фамилия")]    
    duration:    Annotated[Optional[int], Field(description="Пароль")]
    teacher_id:  Annotated[Optional[int], Field(description="Пароль")]


class CourseSearchSchema(BaseModel):
    """Модель [Pydantic] "Для поиска"
    
    """
    name:        str = ""
    description: str = ""
    duration:    int = None
    teacher_id:  int = None


class CourseSchema(BaseModel):
    """Модель [Pydantic] "Пользователь системы"

    """
    id:          Annotated[Optional[int],                Field(description="Идентификатор", default=None)]
    name:        Annotated[Optional[str],                Field(description="Имя", default="UserName")]
    description: Annotated[Optional[str],                Field(description="Фамилия", default="UserSurName" )]
    duration:    Annotated[Optional[int],                          Field(description="Логин", default="")]
    teacher_id:  Annotated[Optional[int],                          Field(description="Логин", default="")]
