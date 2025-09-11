from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from web.auth import auth_user, create_token
from web.config import settings
from web.users.dependencies import get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user = await auth_user(email, password)
        if user:
            token = create_token({"sub": str(user.id)})
            request.session.update({"token": token})
        return True
        
    async def logout(self, request: Request):
        request.session.clear()
        return True
    
    async def authenticate(self, request: Request):
        token = request.session.get("token")
        
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        
        user = await get_current_user(token)
        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        
        return True
    
authentication_backend = AdminAuth(secret_key=settings.TOKEN_BEARER)