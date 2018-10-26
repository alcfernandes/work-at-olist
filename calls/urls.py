from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(title='Calls API')

from calls.core.urls import router as core_router
router = DefaultRouter()
router.registry.extend(core_router.registry)

urlpatterns = [
    path('', RedirectView.as_view(url='/admin')),
    path('admin/', admin.site.urls),
    path('schema/', schema_view),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
