from web.database import Base
from sqlalchemy import Column, String, Integer, DateTime, Date, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class CourseModel(Base):
    __tablename__ = "course"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)
    teacher_id = Column(Integer, nullable=True)
