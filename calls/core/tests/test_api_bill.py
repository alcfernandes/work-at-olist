from datetime import datetime
import pytz

from rest_framework import status
from rest_framework.test import APITestCase

from freezegun import freeze_time

from calls.core.models.call import CallDetail


class APIBillListTest(APITestCase):
    """
    (GET) /api/bill/?subscriber=<source>&period=<MM/YYYY>
    Should return the Subscriber Telephone Bill for the period informed
    """
    fixtures = ['pricingrule.json']

    def setUp(self):

        # Input a Detail Start Record (Reference: 08/2018)
        CallDetail.objects.create(
            id=7001,
            type=CallDetail.START,
            timestamp=datetime(2018, 7, 31, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        # Input a Detail End Record (Reference: 08/2018)
        CallDetail.objects.create(
            id=7002,
            type=CallDetail.END,
            timestamp=datetime(2018, 8, 1, 22, 17, 53, tzinfo=pytz.UTC),
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
            timestamp=datetime(2018, 9, 29, 21, 57, 13, tzinfo=pytz.UTC),
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

    def test_response_with_period(self):
        self.response = self.client.get('/api/bill/?subscriber=99988526423&period=09/2018')

        expected_response = {
            "subscriber": "99988526423",
            "period": "09/2018",
            "calls": [
                {
                    "destination": "9933468278",
                    "start_date": "2018-09-29",
                    "start_time": "21:57:13",
                    "duration": "0h20m40s",
                    "price": "0.54"
                }
            ]
        }

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

        expected_response = {
            "subscriber": "99988526423",
            "period": "09/2018",
            "calls": [
                {
                    "destination": "9933468278",
                    "start_date": "2018-09-29",
                    "start_time": "21:57:13",
                    "duration": "0h20m40s",
                    "price": "0.54"
                }
            ]
        }

        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            expected_response
        )

    def test_response_with_start_end_different_months(self):
        """
        A call record belongs to the period in which the call has ended.

        """
        self.response = self.client.get('/api/bill/?subscriber=99988526423&period=08/2018')

        expected_response = {
            "subscriber": "99988526423",
            "period": "08/2018",
            "calls": [
                {
                    "destination": "9933468278",
                    "start_date": "2018-07-31",
                    "start_time": "21:57:13",
                    "duration": "24h20m40s",
                    "price": "86.94"
                }
            ]
        }

        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            expected_response
        )


class APIBillListParametersValidationTest(APITestCase):
    """
    (GET) /api/bill/?subscriber=<source>&period=<MM/YYYY>
    Should validate the Subscriber and Period parameters
    """
    @freeze_time("2018-10-20")
    def test_get_without_parameters(self):
        self.response = self.client.get('/api/bill/')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_message = "Use the subscriber parameter to inform the subscriber's phone number"
        self.assertEqual(expected_message, self.response.data)

    @freeze_time("2018-10-20")
    def test_get_with_subscriber_without_period(self):
        self.response = self.client.get('/api/bill/?subscriber=99988526423')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    @freeze_time("2018-10-20")
    def test_get_with_period_no_ended(self):
        self.response = self.client.get('/api/bill/?subscriber=99988526423&period=10/2018')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_message = "You can only get bills which period are already closed"
        self.assertEqual(expected_message, self.response.data)

    def test_get_with_period_without_subscriber(self):
        self.response = self.client.get('/api/bill/?period=10/2018')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_message = "Use the subscriber parameter to inform the subscriber's phone number"
        self.assertEqual(expected_message, self.response.data)

    def test_get_with_invalid_subscriber(self):
        self.response = self.client.get('/api/bill/?subscriber=ZZZ88526423')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_message = "Invalid subscriber. Length of 10 to 11 characters, only digits"
        self.assertEqual(expected_message, self.response.data)

    def test_get_with_invalid_period(self):
        self.response = self.client.get('/api/bill/?subscriber=1234567890&period=xx')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_message = "Invalid format for the period. Enter the month and year in MM/YYYY format"
        self.assertEqual(expected_message, self.response.data)
