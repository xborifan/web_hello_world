from fastapi import APIRouter
from time import sleep
from asyncio import sleep as asleep
from random import randint


router = APIRouter(
    prefix="",
    tags=["Синхронные/асинхронные запросы"]
)

@router.get("/test_sync/{id}")
def test_sync(id: int):
    """Для тестов. Синхронное выполнение
    
    """
    timeToWait = randint(3, 10)
    print(f"Получена {id}, исполнится за {timeToWait} сек.")    
    sleep(timeToWait)
    print(f"{id} Завершена")
    return f"Задача {id}, выполнена за {timeToWait} сек."

@router.get("/test_async/{id}")
async def test_async(id: int):
    """Для тестов. Асинхронное выполнение
    
    """    
    timeToWait = randint(3, 10)
    print(f"Получен {id}, исполнится за {timeToWait} сек.")    
    await asleep(timeToWait)
    print(f"{id} Завершена")
    return f"Задача {id}, выполнена за {timeToWait} сек."