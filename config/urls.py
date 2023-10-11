from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.views.generic import RedirectView

from config import settings

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]


schema_view = get_schema_view(
   openapi.Info(
      title="Dizi-izi API",
      default_version='v1',
      description="Документация для проекта Dizi-izi-backend",
      # terms_of_service="URL страницы с пользовательским соглашением",
      contact=openapi.Contact(email="dizi.izi.plan@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('',
         RedirectView.as_view(url='swagger/', permanent=False),
         name='index'),
]


# urlpatterns += [
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     path(
#         'api/schema/swagger-ui/',
#         SpectacularSwaggerView.as_view(url_name='schema'),
#         name='swagger-ui',
#     ),
# ]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
