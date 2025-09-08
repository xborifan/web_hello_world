from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from web.users.router import router as users_router


app = FastAPI()
app.include_router(users_router)

@app.get("/")
def read_root():
    return RedirectResponse("/docs")
