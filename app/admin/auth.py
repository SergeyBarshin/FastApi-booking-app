from app.exсeptions import IncorrectEmailOrPassword
from app.users.auth import authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await authenticate_user(email, password)
        if user:
            access_tocken = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_tocken})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        if token:
            user = await get_current_user(token)
        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)


        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key="...")
