from web.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped


class CourseModel(Base):
    """Модель [sqlalchemy] 'Курс'
    
    """    
    __tablename__ = "course"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)
    #teacher_id = Column(Integer, nullable=True)
    #teacher_id = mapped_column(ForeignKey("user.id"))
    users = relationship("CourseTeacherModel", uselist=True, backref="course")


class CourseTeacherModel(Base):
    """Модель [sqlalchemy] 'Преподаватель курса'
    
    """    
    __tablename__ = "course_teachers"
    
    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    course_id : Mapped[int] = mapped_column(ForeignKey("course.id"), primary_key=True)