from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin
from redis import asyncio as aioredis

from web.config import settings
from auth.scheme import get_bearer_token
from web.admin.views import UsersAdmin, CoursesAdmin, CourseTeacherAdmin
from web.admin.auth import authentication_backend
from web.database import engine
from web.users.router import router as users_router
from web.courses.router import router as courses_router
from web.images.router import router as images_router
from web.sync_or_async.router import router as sync_async_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.redisUrl, encoding="utf-8")
    FastAPICache.init(RedisBackend(redis=redis), prefix="cache")
    yield
    
app = FastAPI(lifespan=lifespan)

#SECURITY = [Depends(get_bearer_token)]

#app.include_router(users_router, dependencies=SECURITY)
app.include_router(users_router)
#app.include_router(courses_router, dependencies=SECURITY)
app.include_router(courses_router)
app.include_router(sync_async_router)
app.include_router(images_router)

@app.get("/", include_in_schema=False)
def read_root():
    """Стартовой страницы пока нет, перекидывает на документацию
    
    """
    return RedirectResponse("/docs")

admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(CoursesAdmin)
admin.add_view(CourseTeacherAdmin)


