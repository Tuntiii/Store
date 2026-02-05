from ninja import NinjaAPI
from apps.content.api import router as content_router
from django.urls import path
from django.http import JsonResponse
from django.conf import settings
from django.core.exceptions import ValidationError


api = NinjaAPI(docs_url="/docs" if settings.DEBUG else None)


@api.exception_handler(ValidationError)
def validation_errors(request, exc: ValidationError):

    return JsonResponse(
        {"error": {"message": [e["msg"] for e in exc.errors]}}, status=422
    )


api.add_router("/", content_router, tags=["Content"])


urlpatterns = [path("", api.urls)]