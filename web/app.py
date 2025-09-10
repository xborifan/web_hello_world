from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from web.users.router import router as users_router
from web.sync_or_async.router import router as sync_async_router


app = FastAPI()
app.include_router(users_router)
app.include_router(sync_async_router)

@app.get("/", include_in_schema=False)
def read_root():
    """Стартовой страницы пока нет, перекидывает на документацию
    
    """
    return RedirectResponse("/docs")
