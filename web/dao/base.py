from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from typing import List
from web.database import async_session_maker


class BaseDAO:
    """Базовый класс Database Access Oject
    
    """
    model = None
    
    @classmethod
    async def find_by_id(cls, model_id: int):
        """Находит в БД объект по идентификатору
        
        """
        try: 
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(id=model_id)
                result = await session.execute(query)
                x = result.scalars().one_or_none()
                if x:
                    return x
                else:
                    raise NoResultFound()
        except:
            return JSONResponse(
                        status_code = status.HTTP_404_NOT_FOUND, 
                        content = {"details": f"Не удалось найти объект с id: {model_id}"})
            
    @classmethod
    async def add(cls, **data):
        """Добавляет новый объект в БД
        
        """   
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
            
    @classmethod
    async def find_all(cls, **filter_by):
        """Находит в БД все объекты, соотв. наложенной фильтрации
        
        """   
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def del_by_id(cls, model_ids: List[int]):
        """Удаляет в БД объект(ы) по идентификатору 
        
        """
        try:
            async with async_session_maker() as session:
                    # сначала пытаемся получить объекты с переданными id
                    selQuery = select(cls.model).filter(cls.model.id.in_(model_ids))
                    result = await session.execute(selQuery)
                    forDelete = len(result.scalars().all())
                    # если нечего удалять - генерируем exception
                    if forDelete != len(model_ids):
                        raise NoResultFound()
                    else:
                        query = delete(cls.model).filter(cls.model.id.in_(model_ids))
                        await session.execute(query)
                        await session.commit()
            return JSONResponse(
                    status_code = status.HTTP_200_OK, 
                    content = {"details": f"Успешное удаление объекта(ов) с id: {model_ids}"})
        except:
            return JSONResponse(
                        status_code = status.HTTP_400_BAD_REQUEST, 
                        content = {"details": f"Не удалось удалить  объект(ы) с id: {model_ids}"})

    @classmethod
    async def find_by(cls, **filter_by):
        """Находит в БД объект, соотв. наложенной фильтрации
        
        """   
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().one_or_none()
