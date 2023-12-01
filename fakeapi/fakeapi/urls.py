from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("master_system.urls")),
    path("auth/", include("djoser.urls")),
    # JWT-endpoints, to manage JWT-tokens:
    path("auth/", include("djoser.urls.jwt")),
]


schema_view = get_schema_view(
    openapi.Info(
        title="Fake API",
        default_version="v1",
        description="Documentation for Fake API project",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns += [
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
