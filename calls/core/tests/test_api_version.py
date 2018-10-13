from rest_framework import status
from rest_framework.test import APITestCase


class APIGetVersionTest(APITestCase):
    def setUp(self):
        self.response = self.client.get('/api/version/')

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_response(self):
        self.assertTrue(self.response.data['API_Version'])
