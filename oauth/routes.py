from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import include, path
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Auto library",
        default_version='v1',
        description="Пример аудио библиотеки на Джанго",
        contact=openapi.Contact(url="")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('auth/', include('oauth.urls')),
    path('audio/', include('audio.urls')),
]
