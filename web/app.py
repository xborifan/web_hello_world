from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from sqladmin import Admin

from auth.scheme import get_bearer_token
from web.admin.views import UsersAdmin, CoursesAdmin
from web.admin.auth import authentication_backend
from web.database import engine, async_session_maker
from web.users.router import router as users_router
from web.courses.router import router as courses_router
from web.sync_or_async.router import router as sync_async_router


app = FastAPI()

SECURITY = [Depends(get_bearer_token)]

app.include_router(users_router, dependencies=SECURITY)
#app.include_router(users_router)
app.include_router(courses_router, dependencies=SECURITY)
app.include_router(sync_async_router)


@app.get("/", include_in_schema=False)
def read_root():
    """Стартовой страницы пока нет, перекидывает на документацию
    
    """
    return RedirectResponse("/docs")

admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(CoursesAdmin)


