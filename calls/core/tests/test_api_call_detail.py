from rest_framework import status
from rest_framework.test import APITestCase

from calls.core.models.call import CallDetail


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
            'type': CallDetail.END,
            'timestamp': "2016-02-29T14:00:00Z",
            'call_id': 70,
        }

        self.response = self.client.post('/api/call-detail/', payload)

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_response(self):
        expected_response = {
                'url': 'http://testserver/api/call-detail/1/',
                'id': 1,
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


class APIStartTypeCallsDetailsValidationTest(APITestCase):

    def test_on_start_type_calls_details_source_is_required(self):
        """
        A Call Start Record without a source telephone number must be rejected.
        """

        payload = {
            'id': 1,
            'type': CallDetail.START,
            'timestamp': "2016-02-29T12:00:00Z",
            'destination': "9933468278",
            'call_id': 70,
        }

        expected_response = {
            "validation_error": [
                "A start-type call detail record must have a source telephone number."
            ]
        }

        response = self.client.post('/api/call-detail/', payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_response
        )

    def test_on_start_type_calls_details_destination_is_required(self):
        """
        A Call Start Record without a destination telephone number must be rejected.
        """

        payload = {
            'id': 1,
            'type': CallDetail.START,
            'timestamp': "2016-02-29T12:00:00Z",
            'source': "9933468278",
            'call_id': 70,
        }

        expected_response = {
            "validation_error": [
                "A start-type call detail record must have a destination telephone number."
            ]
        }

        response = self.client.post('/api/call-detail/', payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_response
        )


class APIEndTypeCallsDetailsValidationTest(APITestCase):

    def test_on_end_type_calls_details_source_and_destination_are_not_required(self):
        """
        For an end-type call detail record, source and destination fields should not be required
        """

        payload = {
            'id': 1,
            'type': CallDetail.END,
            'timestamp': "2016-02-29T12:00:00Z",
            'call_id': 70,
        }

        expected_response = {
            'url': 'http://testserver/api/call-detail/1/',
            'id': 1,
            'type': CallDetail.END,
            'timestamp': "2016-02-29T12:00:00Z",
            'source': None,
            'destination': None,
            'call_id': 70
        }

        response = self.client.post('/api/call-detail/', payload)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_response
        )

    def test_on_end_type_calls_details_source_is_not_expected(self):
        """
        A end-type Call Detail Record should not have a source telephone number.
        """

        payload = {
            'id': 1,
            'type': CallDetail.END,
            'timestamp': "2016-02-29T12:00:00Z",
            'source': "9933468278",
            'call_id': 70,
        }

        expected_response = {
            "validation_error": [
                "A end-type call detail record should not have a source telephone number."
            ]
        }

        response = self.client.post('/api/call-detail/', payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_response
        )

    def test_on_end_type_calls_details_destination_is_not_expected(self):
        """
        A end-type Call Detail Record should not have a destination telephone number.
        """

        payload = {
            'id': 1,
            'type': CallDetail.END,
            'timestamp': "2016-02-29T12:00:00Z",
            'destination': "9933468278",
            'call_id': 70,
        }

        expected_response = {
            "validation_error": [
                "A end-type call detail record should not have a destination telephone number."
            ]
        }

        response = self.client.post('/api/call-detail/', payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_response
        )
