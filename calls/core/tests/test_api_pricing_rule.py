
from rest_framework import status
from rest_framework.test import APITestCase

from calls.core.models.pricing_rule import PricingRule


class APIPricingRuleListTest(APITestCase):
    """
    (GET) /api/pricing/
    Should return the existing Pricing Rules list
    """
    fixtures = ['pricingrule.json']
    
    def setUp(self):
        self.response = self.client.get('/api/pricing/')

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_response(self):
        expected_response = [
            {
                "url": "http://testserver/api/pricing/1/",
                "id": 1,
                "name": "Standard time call",
                "start_time": "06:00:00",
                "end_time": "22:00:00",
                "standing_charge": "0.36",
                "minute_call_charge": "0.09"
            },
            {
                "url": "http://testserver/api/pricing/2/",
                "id": 2,
                "name": "Reduced tariff time call",
                "start_time": "22:00:00",
                "end_time": "06:00:00",
                "standing_charge": "0.36",
                "minute_call_charge": "0.00"
            }
        ]

        self.maxDiff = None
        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            expected_response
        )


class APIPricingRuleCreateTest(APITestCase):
    """
    (POST) /api/pricing/
    It should create a pricing rule record
    """

    def setUp(self):

        payload = {
            "name": "Standard time call",
            "start_time": "06:00:00",
            "end_time": "22:00:00",
            "standing_charge": "0.36",
            "minute_call_charge": "0.09"
        }

        self.response = self.client.post('/api/pricing/', payload)

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_response(self):
        expected_response = {
            "url": "http://testserver/api/pricing/1/",
            "id": 1,
            "name": "Standard time call",
            "start_time": "06:00:00",
            "end_time": "22:00:00",
            "standing_charge": "0.36",
            "minute_call_charge": "0.09"
        }
        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            expected_response
        )


class APIPricingRuleRetrieveTest(APITestCase):
    """
    (GET) /api/pricing/<pricing_rule_id>
    Should return the Pricing Rule Record
    """
    
    fixtures = ['pricingrule.json']
    
    def setUp(self):
        self.response = self.client.get('/api/pricing/1/')

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_response(self):
        expected_response = {
            "url": "http://testserver/api/pricing/1/",
            "id": 1,
            "name": "Standard time call",
            "start_time": "06:00:00",
            "end_time": "22:00:00",
            "standing_charge": "0.36",
            "minute_call_charge": "0.09"
        }

        self.maxDiff = None
        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            expected_response
        )


class APIPricingRuleUpdateTest(APITestCase):
    """
    (PUT) /api/pricing/<call_detail_id>
    Should update and return the Call Details Record
    """

    fixtures = ['pricingrule.json']
    
    def setUp(self):

        payload = {
            "name": "Standard time call",
            "start_time": "06:00:00",
            "end_time": "22:00:00",
            "standing_charge": "0.36",
            "minute_call_charge": "0.09"
        }

        self.response = self.client.put('/api/pricing/1/', payload)

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_response(self):
        expected_response = {
            "url": "http://testserver/api/pricing/1/",
            "id": 1,
            "name": "Standard time call",
            "start_time": "06:00:00",
            "end_time": "22:00:00",
            "standing_charge": "0.36",
            "minute_call_charge": "0.09"
        }

        self.maxDiff = None
        self.assertJSONEqual(
            str(self.response.content, encoding='utf8'),
            expected_response
        )


class APIPricingRuleDeleteTest(APITestCase):
    """
    (DEL) /api/pricing/<pricing_rule_id>
    Should delete the Pricing Rule Record
    """

    fixtures = ['pricingrule.json']
    
    def setUp(self):
        self.response = self.client.delete('/api/pricing/1/')

    def test_get(self):
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete(self):
        self.assertFalse(PricingRule.objects.filter(id=1).exists(), msg="The Pricing Rule should be deleted")

