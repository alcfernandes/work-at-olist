from decimal import Decimal
from datetime import datetime
import pytz

from rest_framework import status
from rest_framework.test import APITestCase


from calls.core.models.call import CallDetail


class APICallList(APITestCase):
    fixtures = ['pricingrule.json']

    def setUp(self):
        # Input a Detail Start Record
        CallDetail.objects.create(
            type=CallDetail.START,
            timestamp=datetime(2016, 2, 29, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        # Input a Detail End Record
        CallDetail.objects.create(
            type=CallDetail.END,
            timestamp=datetime(2016, 2, 29, 22, 17, 53, tzinfo=pytz.UTC),
            call_id=70,
        )

        self.expected = [
            {
                "url": "http://testserver/api/call/70/",
                "id": 70,
                "detail_start": "http://testserver/api/call-detail/1/",
                "detail_end": "http://testserver/api/call-detail/2/",
                "duration": "0h20m40s",
                "price": "0.54"
            },
        ]

        self.response = self.client.get('/api/call/')

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_response(self):
        self.maxDiff = None
        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            self.expected
        )


class APICallRetrieve(APITestCase):
    fixtures = ['pricingrule.json']

    def setUp(self):
        # Input a Detail Start Record
        CallDetail.objects.create(
            type=CallDetail.START,
            timestamp=datetime(2016, 2, 29, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        # Input a Detail End Record
        CallDetail.objects.create(
            type=CallDetail.END,
            timestamp=datetime(2016, 2, 29, 22, 17, 53, tzinfo=pytz.UTC),
            call_id=70,
        )

        self.expected = {
            "url": "http://testserver/api/call/70/",
            "id": 70,
            "detail_start": "http://testserver/api/call-detail/1/",
            "detail_end": "http://testserver/api/call-detail/2/",
            "duration": "0h20m40s",
            "price": "0.54"
        }

        self.response = self.client.get('/api/call/70/')

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_response(self):
        self.maxDiff = None
        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            self.expected
        )
