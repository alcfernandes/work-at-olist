
from rest_framework import viewsets

from rest_framework.response import Response

from calls.api_version import API_Version
from calls.core.models import CallDetail
from calls.core.api.serializers import CallDetailSerializer


class ApiVersion(viewsets.ViewSet):

    def list(self, request):
        return Response({'API_Version': API_Version})


class CallDetailViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = CallDetail.objects.all()
    serializer_class = CallDetailSerializer
