from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import path

from calls.core.api.viewsets import ApiVersion, CallDetailViewSet

app_name = 'core'

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('version', ApiVersion, base_name='version')
router.register('call-detail', CallDetailViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
]
