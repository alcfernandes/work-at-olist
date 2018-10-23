from datetime import datetime

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from calls.api_version import API_Version
from calls.core.models.call import CallDetail, Call
from calls.core.api.serializers import CallDetailSerializer, BillSerializer, CallSerializer
from calls.core.util.helpers import current_month_year


class ApiVersion(viewsets.ViewSet):

    def list(self, request):
        return Response({'API_Version': API_Version})


class CallDetailViewSet(viewsets.ModelViewSet):

    queryset = CallDetail.objects.all()
    serializer_class = CallDetailSerializer


class CallViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Call.objects.all()
    serializer_class = CallSerializer


class BillViewSet(viewsets.ViewSet):

    def list(self, request):
        subscriber = request.GET.get('subscriber', None)
        period = request.GET.get('period', None)

        if subscriber is None:
            msg = "Use the subscriber parameter to inform the subscriber's phone number"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        queryset = Call.objects.filter(detail_start__source=subscriber)

        if period is not None:
            try:
                month_year = datetime.strptime(period, '%m/%Y')
                filter_period = {
                    'detail_end__timestamp__year': month_year.year,
                    'detail_end__timestamp__month': month_year.month
                }

            except ValueError as error:
                msg = 'Invalid format for the period. Enter the month and year in MM/YYYY format'
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)

            if month_year >= current_month_year():
                msg = "You can only get bills which period are already closed"
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        else:
            # Period is not informed. Get the previous month.
            filter_period = {
                'detail_end__timestamp__year': datetime.now().year,
                'detail_end__timestamp__month': datetime.now().month - 1
            }

        queryset = queryset.filter(**filter_period)

        serializer = BillSerializer(queryset, context={'request': request}, many=True)

        return Response(serializer.data)
