import jwt
from datetime import datetime, timedelta, timezone
from django.contrib.auth import authenticate
from django.conf import settings
from ninja import Router
from ninja.security import HttpBearer
from ninja import Schema


class TokenAuth(HttpBearer):
    def authenticate(self, request, token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            from django.contrib.auth.models import User
            return User.objects.get(id=payload["user_id"])
        except (jwt.ExpiredSignatureError, jwt.DecodeError, Exception):
            return None


class SuperUserAuth(HttpBearer):
    def authenticate(self, request, token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            from django.contrib.auth.models import User
            user = User.objects.get(id=payload["user_id"])
            if not user.is_superuser:
                return None
            return user
        except (jwt.ExpiredSignatureError, jwt.DecodeError, Exception):
            return None


def create_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


class TokenRequest(Schema):
    username: str
    password: str


class TokenResponse(Schema):
    token: str


auth_router = Router(tags=["Auth"])


@auth_router.post("/token", response=TokenResponse, auth=None)
def get_token(request, data: TokenRequest):
    user = authenticate(username=data.username, password=data.password)
    if user is None:
        from ninja.errors import HttpError
        raise HttpError(401, "Invalid credentials")
    return {"token": create_token(user.id)}