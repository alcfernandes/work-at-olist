from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import path

from calls.core.api.viewsets import ApiVersion

app_name = 'core'

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('version', ApiVersion, base_name='version')

urlpatterns = [
    path('admin/', admin.site.urls),
]
