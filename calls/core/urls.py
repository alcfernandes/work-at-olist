from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import path

from calls.core.api.viewsets import ApiVersion, CallDetailViewSet, BillViewSet, CallViewSet, PricingRuleViewSet

app_name = 'core'

router = DefaultRouter()
router.register('version', ApiVersion, base_name='version')
router.register('call-detail', CallDetailViewSet)
router.register('bill', BillViewSet, base_name='bill')
router.register('call', CallViewSet, base_name='call')
router.register('pricing', PricingRuleViewSet, base_name='pricingrule')

urlpatterns = [
    path('admin/', admin.site.urls),
]
