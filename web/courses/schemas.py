from pydantic import BaseModel, Field
from typing import Optional, Annotated


class CourseRegSchema(BaseModel):
    """Модель [Pydantic] "Новый курс"
    
    """
    name:        Annotated[str,           Field(description="Название")]
    description: Annotated[Optional[str], Field(description="Описание")]    
    duration:    Annotated[Optional[int], Field(description="Продолжительность")]
    #teacher_id:  Annotated[Optional[int], Field(description="Преподаватель")]


class CourseSearchSchema(BaseModel):
    """Модель [Pydantic] "Курс для поиска"
    
    """
    name:        str = ""
    description: str = ""
    duration:    int = None
    teacher_id:  int = None


class CourseSchema(BaseModel):
    """Модель [Pydantic] "Курс"

    """
    id:          Annotated[Optional[int],                Field(description="Идентификатор", default=None)]
    name:        Annotated[Optional[str],                Field(description="Название", default="")]
    description: Annotated[Optional[str],                Field(description="Описание", default="" )]
    duration:    Annotated[Optional[int],                Field(description="Продолжительность", default="")]
    #teacher_id:  Annotated[Optional[int],                Field(description="Преподаватель", default="")]

