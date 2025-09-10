from web.database import Base
from sqlalchemy import Column, String, Integer


class CourseModel(Base):
    """Модель [sqlalchemy] 'Курс'
    
    """    
    __tablename__ = "course"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)
    teacher_id = Column(Integer, nullable=True)
