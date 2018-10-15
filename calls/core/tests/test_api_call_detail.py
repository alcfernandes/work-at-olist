from rest_framework import status
from rest_framework.test import APITestCase

from calls.core.models import CallDetail


class APIStartCallDetailCreate(APITestCase):
    """
    It should create a call start detail record when receiving a start record post in the endpoint /api/call-detail/
    """

    def setUp(self):

        payload = {
            'id': 1,
            'type': CallDetail.START,
            'timestamp': "2016-02-29T12:00:00Z",
            'source': "99988526423",
            'destination': "9933468278",
            'call_id': 70,
        }

        self.response = self.client.post('/api/call-detail/', payload)

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_response(self):
        expected_response = {
                'url': 'http://testserver/api/call-detail/1/',
                'id': 1,
                'type': CallDetail.START,
                'timestamp': "2016-02-29T12:00:00Z",
                'source': "99988526423",
                'destination': "9933468278",
                'call_id': 70
        }
        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            expected_response
        )


class APIEndCallDetailCreate(APITestCase):
    """
    It should create a call start detail record when receiving a end record post in the endpoint /api/call-detail/
    """

    def setUp(self):

        payload = {
            'id': 2,
            'type': CallDetail.END,
            'timestamp': "2016-02-29T14:00:00Z",
            'call_id': 70,
        }

        self.response = self.client.post('/api/call-detail/', payload)

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_response(self):
        expected_response = {
                'url': 'http://testserver/api/call-detail/2/',
                'id': 2,
                'type': CallDetail.END,
                'timestamp': "2016-02-29T14:00:00Z",
                'source': None,
                'destination': None,
                'call_id': 70
        }
        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            expected_response
        )
