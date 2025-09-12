from web.database import Base
from web.courses.models import CourseTeacherModel
from sqlalchemy import Column, String, Integer, DateTime, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class UserModel(Base):
    """Модель [sqlalchemy] 'Пользователь'
    
    """
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    login = Column(String, nullable=False, unique=True)
    dateOfBirth = Column(Date, nullable=False)
    patronymic = Column(String, nullable=True)
    dateOfReg : Mapped[datetime]  = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    email = Column(String, nullable=True, unique=True)
    phone = Column(String, nullable=True)
    password : Mapped[str]
    
    teacher = relationship("CourseTeacherModel", uselist=True, backref="user")