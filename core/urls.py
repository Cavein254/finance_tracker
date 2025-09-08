from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Finance App API",
        default_version="v1",
        description="Test description",
    ),
    public=True,
    authentication_classes=[],
    permission_classes=[],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("users/", include("users.urls")),
                # swagger
                path(
                    "swagger<format>/",
                    schema_view.without_ui(cache_timeout=0),
                    name="schema-json",
                ),
                path(
                    "swagger/",
                    schema_view.with_ui("swagger", cache_timeout=0),
                    name="schema-swagger-ui",
                ),
                path(
                    "redoc/",
                    schema_view.with_ui("redoc", cache_timeout=0),
                    name="schema-redoc",
                ),
            ]
        ),
    ),
]
