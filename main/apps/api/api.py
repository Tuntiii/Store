from ninja import NinjaAPI
from apps.api.auth import auth_router
from apps.content.api import category_router, model_router

api = NinjaAPI(title="Store API", version="1.0.0")

api.add_router("/auth/", auth_router)
api.add_router("/categories", category_router)
api.add_router("/models", model_router)