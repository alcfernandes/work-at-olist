from decimal import Decimal
from datetime import datetime, time
import pytz

from rest_framework import status
from rest_framework.test import APITestCase

from freezegun import freeze_time

from calls.core.models.call import CallDetail
from calls.core.models.pricing_rule import PricingRule


class APIBillList(APITestCase):
    """
    Should return the Telephone Bill in response a /api/bill/?subscriber=<telephone>&period=<month/year>
    """

    def setUp(self):
        # Input Pricing Rules
        PricingRule.objects.create(
            id=1,
            name="Standard time call",
            start_time=time(6, 0, 0),
            end_time=time(22, 0, 0),
            standing_charge=Decimal(0.36),
            minute_call_charge=Decimal(0.09),
        )

        PricingRule.objects.create(
            id=2,
            name="Reduced tariff time call",
            start_time=time(22, 0, 0),
            end_time=time(6, 0, 0),
            standing_charge=Decimal(0.36),
            minute_call_charge=Decimal(0.00),
        )

        # Input a Detail Start Record (Reference: 08/2018)
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=datetime(2018, 8, 29, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        # Input a Detail End Record (Reference: 08/2018)
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=datetime(2018, 8, 29, 22, 17, 53, tzinfo=pytz.UTC),
            call_id=70,
        )

        # Input a Detail Start Record (Reference: 09/2018)
        CallDetail.objects.create(
            id=8001,
            type=CallDetail.START,
            timestamp=datetime(2018, 9, 29, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=80,
        )

        # Input a Detail End Record (Reference: 09/2018)
        CallDetail.objects.create(
            id=8002,
            type=CallDetail.END,
            timestamp=datetime(2018, 9, 29, 22, 17, 53, tzinfo=pytz.UTC),
            call_id=80,
        )

        # Input a Detail Start Record (Reference: 10/2018)
        CallDetail.objects.create(
            id=9001,
            type=CallDetail.START,
            timestamp=datetime(2018, 10, 29, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=90,
        )

        # Input a Detail End Record (Reference: 10/2018)
        CallDetail.objects.create(
            id=9002,
            type=CallDetail.END,
            timestamp=datetime(2018, 10, 29, 22, 17, 53, tzinfo=pytz.UTC),
            call_id=90,
        )

    def test_get_with_period(self):
        self.response = self.client.get('/api/bill/?subscriber=99988526423&period=09/2018')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    @freeze_time("2018-10-20")
    def test_get_without_period(self):
        self.response = self.client.get('/api/bill/?subscriber=99988526423')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    @freeze_time("2018-10-20")
    def test_get_without_parameters(self):
        self.response = self.client.get('/api/bill/')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_message = "Use the subscriber parameter to inform the subscriber's phone number"
        self.assertEqual(expected_message, self.response.data)

    @freeze_time("2018-10-20")
    def test_get_with_period_no_ended(self):
        self.response = self.client.get('/api/bill/?subscriber=99988526423&period=10/2018')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_message = "You can only get bills which period are already closed"
        self.assertEqual(expected_message, self.response.data)

    def test_response_with_period(self):
        self.response = self.client.get('/api/bill/?subscriber=99988526423&period=09/2018')
        expected_response = [
            {
                'destination': "9933468278",
                'start_date': "2018-09-29",
                'start_time': "21:57:13",
                'duration': "0h20m40s",
                'price': "0.54"
            },
        ]
        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            expected_response
        )

    @freeze_time("2018-10-20")
    def test_response_without_period(self):
        """
        Without period parameter should return the last month bill (09/2018).
        """
        self.response = self.client.get('/api/bill/?subscriber=99988526423')
        expected_response = [
            {
                'destination': "9933468278",
                'start_date': "2018-09-29",
                'start_time': "21:57:13",
                'duration': "0h20m40s",
                'price': "0.54"
            },
        ]
        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            expected_response
        )
