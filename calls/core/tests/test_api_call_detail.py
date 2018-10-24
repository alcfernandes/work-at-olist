from datetime import datetime
import pytz

from rest_framework import status
from rest_framework.test import APITestCase

from calls.core.models.call import CallDetail


class APICallDetailListTest(APITestCase):
    """
    (GET) /api/call-detail/
    Should return the existing Call Details list
    """

    def setUp(self):

        # Input a Detail Start Record (Reference: 08/2018)
        CallDetail.objects.create(
            type=CallDetail.START,
            timestamp=datetime(2018, 7, 31, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        # Input a Detail End Record (Reference: 08/2018)
        CallDetail.objects.create(
            type=CallDetail.END,
            timestamp=datetime(2018, 8, 1, 22, 17, 53, tzinfo=pytz.UTC),
            call_id=70,
        )

        self.response = self.client.get('/api/call-detail/')

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_response(self):
        expected_response = [
            {
                "url": "http://testserver/api/call-detail/1/",
                "id": 1,
                "type": "start",
                "timestamp": "2018-07-31T21:57:13Z",
                "source": "99988526423",
                "destination": "9933468278",
                "call_id": 70
            },
            {
                "url": "http://testserver/api/call-detail/2/",
                "id": 2,
                "type": "end",
                "timestamp": "2018-08-01T22:17:53Z",
                "source": None,
                "destination": None,
                "call_id": 70
            }
        ]

        self.maxDiff = None
        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            expected_response
        )


class APIStartCallDetailCreateTest(APITestCase):
    """
    (POST) /api/call-detail/
    It should create a call start detail record when receiving a start type record
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


class APIEndCallDetailCreateTest(APITestCase):
    """
    (POST) /api/call-detail/
    It should create a call start detail record when receiving a end type record
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


class APICallDetailRetrieveTest(APITestCase):
    """
    (GET) /api/call-detail/<call_detail_id>
    Should return the Call Details Record
    """

    def setUp(self):

        # Input a Detail Start Record (Reference: 08/2018)
        CallDetail.objects.create(
            type=CallDetail.START,
            timestamp=datetime(2018, 7, 31, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        self.response = self.client.get('/api/call-detail/1/')

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_response(self):
        expected_response = {
            "url": "http://testserver/api/call-detail/1/",
            "id": 1,
            "type": "start",
            "timestamp": "2018-07-31T21:57:13Z",
            "source": "99988526423",
            "destination": "9933468278",
            "call_id": 70
        }

        self.maxDiff = None
        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            expected_response
        )


class APICallDetailUpdateTest(APITestCase):
    """
    (PUT) /api/call-detail/<call_detail_id>
    Should update and return the Call Details Record
    """

    def setUp(self):

        CallDetail.objects.create(
            type=CallDetail.START,
            timestamp=datetime(2018, 7, 31, 21, 57, 13, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        payload = {
            'type': CallDetail.START,
            'timestamp': "2016-02-20T12:00:00Z",
            'source': "99988526423",
            'destination': "9933468278",
            'call_id': 70,
        }

        self.response = self.client.put('/api/call-detail/1/', payload)

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_response(self):
        expected_response = {
            "url": "http://testserver/api/call-detail/1/",
            "id": 1,
            "type": "start",
            "timestamp": "2016-02-20T12:00:00Z",
            "source": "99988526423",
            "destination": "9933468278",
            "call_id": 70
        }

        self.maxDiff = None
        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            expected_response
        )


class APICallDetailDeleteTest(APITestCase):
    """
    (DEL) /api/call-detail/<call_detail_id>
    Should delete the Call Details Record
    """

    def setUp(self):

        self.start_detail = CallDetail.objects.create(
            id=1,
            type=CallDetail.START,
            timestamp=datetime(2016, 2, 29, 12, 00, 00, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        self.response = self.client.delete('/api/call-detail/1/')

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete(self):
        self.assertFalse(CallDetail.objects.exists(), msg="The Call detail should be deleted")


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

    def test_on_start_type_calls_details_source_only_numbers_validation(self):
        """
        A source telephone number with wrong format must be rejected.
        """

        payload = {
            'id': 1,
            'type': CallDetail.START,
            'timestamp': "2016-02-29T12:00:00Z",
            'source': "XY999999999",
            'destination': "9933468278",
            'call_id': 70,
        }

        expected_response = {
            "source": [
                "Only numbers are allowed."
            ]
        }

        response = self.client.post('/api/call-detail/', payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_response
        )

    def test_on_start_type_calls_details_destination_only_numbers_validation(self):
        """
        A destination telephone number with wrong format must be rejected.
        """

        payload = {
            'id': 1,
            'type': CallDetail.START,
            'timestamp': "2016-02-29T12:00:00Z",
            'source': "9933468278",
            'destination': "XY999999999",
            'call_id': 70,
        }

        expected_response = {
            "destination": [
                "Only numbers are allowed."
            ]
        }

        response = self.client.post('/api/call-detail/', payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_response
        )

    def test_on_start_type_calls_details_source_max_length_validation(self):
        """
        A source telephone number with more than 11 digits must be rejected.
        """

        payload = {
            'id': 1,
            'type': CallDetail.START,
            'timestamp': "2016-02-29T12:00:00Z",
            'source': "123456789012",
            'destination': "12345678901",
            'call_id': 70,
        }

        expected_response = {
            "source": [
                "Ensure this field has no more than 11 characters."
            ]
        }

        response = self.client.post('/api/call-detail/', payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_response
        )

    def test_on_start_type_calls_details_destination_max_length_validation(self):
        """
        A destination telephone number with more than 11 digits must be rejected.
        """

        payload = {
            'id': 1,
            'type': CallDetail.START,
            'timestamp': "2016-02-29T12:00:00Z",
            'source': "12345678901",
            'destination': "123456789012",
            'call_id': 70,
        }

        expected_response = {
            "destination": [
                "Ensure this field has no more than 11 characters."
            ]
        }

        response = self.client.post('/api/call-detail/', payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_response
        )

    def test_on_start_type_calls_details_source_min_length_validation(self):
        """
        A source telephone number with less than 10 digits must be rejected.
        """

        payload = {
            'id': 1,
            'type': CallDetail.START,
            'timestamp': "2016-02-29T12:00:00Z",
            'source': "123456789",
            'destination': "12345678901",
            'call_id': 70,
        }

        expected_response = {
            "source": [
                "Ensure this field has at least 10 characters."
            ]
        }

        response = self.client.post('/api/call-detail/', payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_response
        )

    def test_on_start_type_calls_details_destination_min_length_validation(self):
        """
        A destination telephone number with less than 10 digits must be rejected.
        """

        payload = {
            'id': 1,
            'type': CallDetail.START,
            'timestamp': "2016-02-29T12:00:00Z",
            'source': "12345678901",
            'destination': "123456789",
            'call_id': 70,
        }

        expected_response = {
            "destination": [
                "Ensure this field has at least 10 characters."
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

    def test_on_start_type_calls_details_source_and_destination_must_be_different(self):
        """
        The same phone number for source and destination should be rejected
        """

        payload = {
            'id': 1,
            'type': CallDetail.START,
            'timestamp': "2016-02-29T12:00:00Z",
            'source': "9933468278",
            'destination': "9933468278",
            'call_id': 70,
        }

        expected_response = {
            "validation_error": [
                "Source and destination telephone number must be different."
            ]
        }

        response = self.client.post('/api/call-detail/', payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_response
        )

    def test_start_end_type_oder_validation(self):
        """
        A end call detail record timestamp before than start call detail record timestamp should be rejected.
        """

        CallDetail.objects.create(
            type=CallDetail.START,
            timestamp=datetime(2016, 2, 29, 12, 00, 00, tzinfo=pytz.UTC),
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        payload = {
            'id': 1,
            'type': CallDetail.END,
            'timestamp': datetime(2016, 2, 29, 10, 00, 00, tzinfo=pytz.UTC),
            'call_id': 70,
        }

        expected_response = {
            "validation_error": "The End Call Detail record must be after than the Start Call Detail record"
        }

        response = self.client.post('/api/call-detail/', payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_response
        )

    def test_end_start_type_oder_validation(self):
        """
        A start call detail record timestamp after than ebd call detail record timestamp should be rejected.
        """

        CallDetail.objects.create(
            type=CallDetail.END,
            timestamp=datetime(2016, 2, 29, 12, 00, 00, tzinfo=pytz.UTC),
            call_id=70,
        )

        payload = {
            'id': 1,
            'type': CallDetail.START,
            'source': "99988526423",
            'destination': "9933468278",
            'timestamp': datetime(2016, 2, 29, 13, 00, 00, tzinfo=pytz.UTC),
            'call_id': 70,
        }

        expected_response = {
            "validation_error": "The Start Call Detail record must be before than the End Call Detail record"
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
        For an end type call detail record, source and destination fields should not be required
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
        An end type Call Detail Record should not have a source telephone number.
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
        An end type Call Detail Record should not have a destination telephone number.
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


class APICallDetailCreateUniqueTypeCallValidation(APITestCase):
    """
    Case client try to resubmit a record detail of start or end of a call it should be rejected.
    """

    def setUp(self):
        CallDetail.objects.create(
            type=CallDetail.START,
            timestamp="2016-02-29T12:00:00Z",
            source="99988526423",
            destination="9933468278",
            call_id=70,
        )

        payload = {
            'type': CallDetail.START,
            'timestamp': "2016-02-29T10:00:00Z",
            'source': "99988526423",
            'destination': "9933468278",
            'call_id': 70,
        }

        self.response = self.client.post('/api/call-detail/', payload)

    def test_unique_type_validation_on_post(self):
        expected_response = {
            "validation_error": [
                "A detail record with this type and call id has already been sent. Delete it before resend it."
            ]
        }

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            expected_response
        )

